from loguru import logger
from element.Element import RuntimeActionableElement, ActionableElement
from element.operators import get_style, apply_style, highlight_element
from page.extractor import extract_page_info, save_screenshot, get_place

from page.page import PageData
from utils import randomword
from pathlib import Path
from element.Element import RuntimeActionableElement, ActionableElement

from urllib.parse import urlparse

class Validation:
    def __init__(self, base_domain):
        self.base_domain = base_domain
        pass

    def on_crawl_start(self, driver):
        pass

    def on_navigation_step_start(self, driver):
        pass

    def on_parse_html_start(self, driver):
        if urlparse(driver.current_url).netloc != self.base_domain:
            raise Exception("Out of domain detected !")

    def on_parse_html_end(self, driver, pdata: PageData):
        if pdata.num_objects == 0:
            raise Exception("Not found any actionable element in the current page")

    def on_push_object_end(self, elements: list[ActionableElement]):
        pass

    def on_create_mask_end(self, candidate_masks: list[bool]):
        if True not in candidate_masks:
            raise Exception("No actionable element candidates for this page ~(fully covered)")

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