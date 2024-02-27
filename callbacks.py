from loguru import logger
from element.Element import RuntimeActionableElement, ActionableElement
from element.operators import get_style, apply_style, highlight_element
from page.extractor import extract_page_info, save_screenshot, get_place

from page.page import PageData
from utils import randomid
from pathlib import Path
from element.Element import RuntimeActionableElement, ActionableElement
from petrinet.PetriNet import ActionableTransition, Place, PetriNet

import os

class Callback:
    def __init__(self, working_dir, petriNet, init_place):
        self.working_dir = working_dir
        self.petriNet = petriNet
        self.init_place = init_place
        pass

    def on_crawl_start(self, driver):
        pass

    def on_navigation_step_start(self, driver):
        pass

    def on_parse_html_start(self, driver):
        pass

    def on_parse_html_end(self, driver, pdata: PageData):
        pass

    def on_push_object_end(self, elements: list[ActionableElement]):
        pass

    def on_create_mask_end(self, candidate_masks: list[bool]):
        pass

    def on_select_action_start(self, elements:list[ActionableElement], candidate_masks: list[bool]):
        pass

    def on_execute_action_start(self, driver, selected_element: RuntimeActionableElement):
        pass

    def on_execute_action_end(self, selected_element: RuntimeActionableElement):
        pass

    def on_navigation_step_end(self, selected_element, pdata):
        pass

    def on_crawl_end(self, driver):
        pass


class PetriNetBuilderCallback(Callback):

    def on_crawl_start(self, driver):
        self.__previous_transition = None
        self.__previous_place = self.init_place
        self.__current_place = None
        pass

    def on_parse_html_start(self, driver):
        self.__place_name = f"P{randomid()}"
        self.__save_dir = os.path.join(self.working_dir, "places", self.__place_name)
        Path(self.__save_dir).mkdir(parents=True, exist_ok=True)

    def on_parse_html_end(self, driver, pdata: PageData):
        pdata.screenshot = save_screenshot(driver, self.__save_dir)
        logger.info( f"-- title: [{pdata.title}], url: [{pdata.url}], # total_objects: [{pdata.num_objects}]")
        pass

    def on_push_object_end(self, elements: list[ActionableElement]):
        pass

    def on_create_mask_end(self, candidate_masks: list[bool]):
        num_candidates = len([c for c in candidate_masks if c == True])
        logger.info(f"-- #total actionable candidates: {num_candidates}")

    def on_select_action_start(self, elements:list[ActionableElement], candidate_masks: list[bool]):
        self.__selected_element_screenshot = None
        pass

    def on_execute_action_start(self, driver, selected_element: RuntimeActionableElement):
        # store the current CSS style
        self.__original_style = get_style(selected_element._runtime_element)
        highlight_element(selected_element._runtime_element)
        self.__selected_element_screenshot = save_screenshot(driver,
                                                        save_path=os.path.join(self.working_dir, "screenshots"),
                                                        filename=selected_element.get_attribute('uuid') + ".png")
        selected_element._element.generate_xpath_attributes(selected_element._runtime_element, driver)

    def on_execute_action_end(self, selected_element: RuntimeActionableElement):
        if selected_element.is_attached():
            apply_style(selected_element._runtime_element, self.__original_style)


    def on_navigation_step_end(self, selected_element, pdata, arc_data=[None]):
        selected_event = selected_element.action.name
        transition_data = selected_element.to_actionable_element()
        transition_data._all_attributes['screenshot'] = self.__selected_element_screenshot
        next_transition = ActionableTransition(name=f"T{randomid()}",
                                               node_data=transition_data, transition_type=selected_event)

        if self.init_place is not None and self.__current_place is None:
            self.__current_place = self.init_place
        else:
            self.__current_place = Place(self.__place_name, data=pdata)
            self.petriNet.add_node(self.__current_place)

        self.petriNet.add_node(next_transition)
        self.petriNet.add_arc(self.petriNet.node(self.__current_place.name), self.petriNet.node(next_transition.name))
        logger.debug(f"-- connect {self.__current_place.name} to (next) {next_transition.name}")

        if self.__previous_transition is not None:
            self.petriNet.add_arc(self.petriNet.node(self.__previous_transition.name), self.petriNet.node(self.__current_place.name), data=arc_data)
            logger.debug(f"-- connect (prev) {self.__previous_transition.name} to {self.__current_place.name}")

        self.__previous_transition, self.__previous_place = next_transition, self.__current_place
        PetriNet.save(self.petriNet, f"{self.working_dir}/petri-net.pkl")
        pdata.export(filename=os.path.join(self.__save_dir, "info.json"))

    def on_crawl_end(self, driver):
        pass



class UserTrackingPetriNetBuilderCallback(Callback):

    def on_crawl_start(self, driver):
        self.__previous_transition = None
        self.__previous_place = self.init_place
        self.__current_place = None
        pass

    def on_parse_html_start(self, driver):
        self.__place_name = f"P{randomid()}"
        self.__save_dir = os.path.join(self.working_dir, "places", self.__place_name)
        Path(self.__save_dir).mkdir(parents=True, exist_ok=True)

    def on_parse_html_end(self, driver, pdata: PageData):
        pdata.screenshot = save_screenshot(driver, self.__save_dir)
        logger.info( f"-- title: [{pdata.title}], url: [{pdata.url}], # total_objects: [{pdata.num_objects}]")
        pass

    def on_push_object_end(self, elements: list[ActionableElement]):
        pass

    def on_create_mask_end(self, data=None):
        pass

    def on_select_action_start(self, elements:list[ActionableElement], candidate_masks: list[bool]):
        self.__selected_element_screenshot = None
        pass

    def on_execute_action_start(self, driver, selected_element: RuntimeActionableElement):
        # store the current CSS style
        self.__original_style = get_style(selected_element._runtime_element)
        highlight_element(selected_element._runtime_element)
        self.__selected_element_screenshot = save_screenshot(driver,
                                                        save_path=os.path.join(self.working_dir, "screenshots"),
                                                        filename=selected_element.get_attribute('uuid') + ".png")
        selected_element._element.generate_xpath_attributes(selected_element._runtime_element, driver)

    def on_execute_action_end(self, selected_element: RuntimeActionableElement):
        if selected_element.is_attached():
            apply_style(selected_element._runtime_element, self.__original_style)


    def on_navigation_step_end(self, selected_element, pdata, arc_data=[None]):
        selected_event = selected_element.action.name
        transition_data = selected_element.to_actionable_element()
        transition_data._all_attributes['screenshot'] = self.__selected_element_screenshot
        next_transition = ActionableTransition(name=f"T{randomid()}",
                                               node_data=transition_data, transition_type=selected_event)

        if self.init_place is not None and self.__current_place is None:
            self.__current_place = self.init_place
        else:
            self.__current_place = Place(self.__place_name, data=pdata)
            self.petriNet.add_node(self.__current_place)

        self.petriNet.add_node(next_transition)
        self.petriNet.add_arc(self.petriNet.node(self.__current_place.name), self.petriNet.node(next_transition.name), data=arc_data)
        logger.debug(f"-- connect {self.__current_place.name} to (next) {next_transition.name}")

        if self.__previous_transition is not None:
            self.petriNet.add_arc(self.petriNet.node(self.__previous_transition.name), self.petriNet.node(self.__current_place.name))
            logger.debug(f"-- connect (prev) {self.__previous_transition.name} to {self.__current_place.name}")

        self.__previous_transition, self.__previous_place = next_transition, self.__current_place
        PetriNet.save(self.petriNet, f"{self.working_dir}/petri-net.pkl")
        pdata.export(filename=os.path.join(self.__save_dir, "info.json"))

    def on_crawl_end(self, driver):
        pass

