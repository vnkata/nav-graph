from collections import namedtuple
from typing import Dict, List, Union
from loguru import logger
from petrinet.PetriNet import  Place, Transition, PetriNet
import random
Trajectory = namedtuple('Trajectory', ['transitions', 'places'])

def create_trajectory(target: Place) -> Trajectory:
    """
    Create a trajectory (a list of transitions and places) 
    from root node to @target place
    """
    
    path = {'transitions': [], 'places': []}
    curr = target
    while len(list(curr.input_arc())) == 1:
        transition = list(curr.input_arc())[0].source
        path['transitions'].append(transition)
        path['places'].append(curr)
        curr = list(transition.input_arc())[0].source
    
    path['places'].append(curr)
    
    # reverse order
    _all_places = path['places']
    _all_places.reverse()

    _all_transitions = path['transitions']
    _all_transitions.reverse()
    return Trajectory(transitions=_all_transitions, places=_all_places)

# def select_random_path(petriNet: PetriNet)-> list[Transition]:
#     selected_path = {'transitions': [], 'places': []}
#     current_place:Place = petriNet.root[random.choice(list(range(len(petriNet.root))))]
#     selected_path['places'].append(current_place)
#     while (len(current_place.output_arc()) >= 1):
#         if len(current_place.output_arc()) == 1:
#             next_transition: Transition = list(current_place.output_arc())[0].destination
#         else:
#             next_transition: Transition = random.choice(list(current_place.output_arc())).destination

#         if len(next_transition.output_arc()) > 0:
#             current_place = list(next_transition.output_arc())[0].destination
#             selected_path['transitions'].append(next_transition)
#             selected_path['places'].append(current_place)
#         else:
#             selected_path['transitions'].append(next_transition)
#             break
#     return selected_path

def select_random_path(petriNet: PetriNet)-> Trajectory:
    selected_path = {'transitions': [], 'places': []}
    current_place:Place = petriNet.root[random.choice(list(range(len(petriNet.root))))]
    selected_path['places'].append(current_place)
    while (len(current_place.output_arc()) >= 1):
        if len(current_place.output_arc()) == 1:
            next_transition: Transition = list(current_place.output_arc())[0].destination
        else:
            next_transition: Transition = random.choice(list(current_place.output_arc())).destination

        if len(next_transition.output_arc()) > 0:
            current_place = list(next_transition.output_arc())[0].destination
            selected_path['transitions'].append(next_transition)
            selected_path['places'].append(current_place)
        else:
            selected_path['transitions'].append(next_transition)
            break
    return Trajectory(transitions=selected_path['transitions'], places=selected_path['places'])

def generate_path(petriNet: PetriNet)-> Trajectory:
    selected_path = {'transitions': [], 'places': []}
    current_place:Place = petriNet.root[0]
    selected_path['places'].append(current_place)
    while (len(current_place.output_arc()) >= 1):
        next_transition: Transition = list(current_place.output_arc())[0].destination

        if len(next_transition.output_arc()) > 0:
            current_place = list(next_transition.output_arc())[0].destination
            selected_path['transitions'].append(next_transition)
            selected_path['places'].append(current_place)
        else:
            selected_path['transitions'].append(next_transition)
            break
    return Trajectory(transitions=selected_path['transitions'], places=selected_path['places'])

# def find_next_transition(current_place:Place, target_transition: str, petriNet: PetriNet) -> Union[Transition,None]:
#     """Find the next transition object which has the transition.name == target_transition 
#     from the `current_place` """

#     if len(current_place.data['selected']) > 0:
#         history_info = [data['next_transition'] for data in current_place.data['selected'] 
#                 if data['next_transition'] == target_transition]
#         if len(history_info) == 1:
#             return petriNet.transition(history_info[0])
#         else:
#             logger.info("Not found any transition to go next. Finish !!!")
#             return None
#     else:
#         for tr in current_place.output_arc():
#             if tr.destination.name  == target_transition:
#                 return tr.destination
#         return None