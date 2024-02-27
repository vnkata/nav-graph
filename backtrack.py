from collections import namedtuple
from functools import partial
from typing import Union

from petrinet.PetriNet import Place, Transition, PetriNet
from petrinet.traversal_utils import create_trajectory
from element.Element import ActionableElement, RuntimeActionableElement
from comparators.cmp_place import LessStrictPlaceComparator
from element.operators import find_element
from page.extractor import  get_place
from repository.core import ObjectManager

from loguru import logger

def fast_backtrack(driver, petriNet: PetriNet, objManager: ObjectManager, target: Place, place_cmp) -> Place:
    """
    Backtrack with the help of the current Petri-Net information.
    We use Petri-Net to navigate the WebDriver to the (@target) place.
    (@place_compator) is used mainly to compare the current (runtime) page 
    with the previous stored state/page in the Petri-Net.
    """
    
    trajectory = create_trajectory(target)
    logger.info (f"navigate to state~{target} from root node, trajectory: {trajectory}")
    current_place = trajectory.places[0] #petriNet.root[0]
    driver.get(current_place.data.url)

    if len(trajectory.transitions) == 0:
        logger.debug (f"no transition in the trajectory!, return root place~({str(petriNet.root)})")
        return petriNet.root[0]
    
    for step in range(len(trajectory.places)):
        logger.info(f"Access: current_place=[{current_place.name}], stored_place={trajectory.places[step]}, depth=[{step}]")
        candidate_transitions = []
        for x in current_place.output_arc():
            if x.destination.name == trajectory.transitions[step].name:
                candidate_transitions.append(x.destination)
    
        next_transition: Transition = candidate_transitions[0]
        next_element: ActionableElement = objManager.get_object(next_transition.data.get_attribute('uuid'))
        if len(next_transition.output_arc()) == 0:
            logger.debug(f"transition~({next_transition}) does not contain any output_arc()")
            return current_place

        next_element_rt: RuntimeActionableElement = find_element(next_element, driver) 
        if next_element_rt is None:
            logger.debug(f"element~({next_element.get_attribute('uuid')}) can not found!")
            return current_place
        
        if not next_element_rt.perform(driver):
            logger.debug(f"can not perform action on element~{next_element_rt}")
            return current_place
        
        next_place = [pl.destination for pl in next_transition.output_arc() if pl.destination.name == trajectory.places[step+1].name][0]
        if step +1 == len(trajectory.transitions):
            if place_cmp(get_place(driver, objManager), next_place):
                logger.debug(f"navigate to target place -- success, exit... (found={next_place}, target={target})")
                return next_place
            else:
                logger.info(f"navigate to target place~({next_place}) -- failed, return ~{current_place} instead!")
                return current_place

        current_place =  next_place
    
def backtrack(driver, petriNet: PetriNet, objManager: ObjectManager, target: Place) -> Place:
    """
    An agent may get stuck during crawling as there are no actionable elements to explore next.
    In this case, we must go back to the previous state and continue exploring.
    Going back to the previous state can be performed by:
        (1). Try with the "Back" button first; if the newly obtained page is identical to the (@target) place,
        -- using a given place comparison algorithm --, then the backtracking procedure is completed.
        (2). In case the "Back" button can not bring the WebDriver back to the previous state, we rely on (@petriNet)
        to navigate WebDriver from the root nodes up the (@target) place or the nearest place in the [root-@target] trajectory.
    """

    if target is None:
        logger.debug("Not specify the target place, return [root] place instead")
        return petriNet.root[0]

    if petriNet.root[0] is None:
        logger.debug('The Petri-Net root node is empty.')
        return target

    place_cmp = partial(LessStrictPlaceComparator, objManager=objManager)
    driver.execute_script("window.history.go(-1)")
    if place_cmp(target, get_place(driver, objManager)):
        logger.info("backtracking with #back button successully.")
        return target

    return fast_backtrack(driver, petriNet, objManager, target, place_cmp)