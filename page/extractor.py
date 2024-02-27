import os
from abc import abstractmethod
from functools import partial
from typing import List

import chromedriver_binary
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from comparators.cmp_element import BasicElementComparator, XpathBasedElementComparator
from element.Element import ActionableElement, RuntimeActionableElement, ElementFactory
from page.page import PageData
from repository.core import ObjectManager
from petrinet.PetriNet import Place
from utils import randomword
import time
from loguru import logger

#whether robular, absolute can be regenerated from actionable elements and data from database?
def get_actionable_elements(driver, objectManager, query_value, xpath_included=True, e_comparator = BasicElementComparator()) -> list[RuntimeActionableElement]:
    #filter all of actionable elements before finding into list
    _elements = driver.find_elements(by=By.XPATH, value=query_value)
    _elements = [e for e in _elements if e is not None and e.is_displayed() and e.is_enabled()]

    # the same element attributes excepting for xpath from different step can be unique or not
    # stored_elements = objectManager.get_allobjects()
    #hash([hash_obj.values()['id'], hash_obj.values()[0]['tag_name'], hash_obj.values()[0]['text'], hash_obj.values()[0]['accessible_name']])
    # hashed_list_obj = [hash_obj for hash_obj in stored_elements.values()]

    _elements_q =  list(map(partial(ElementFactory().get, xpath_included=False), _elements))
    new_elements: List[WebElement] = []
    for idx, element_q in enumerate(_elements_q):
        if e_comparator.is_contain(element_q, objectManager.get_by_tagname(element_q.get_attribute('tag_name'))) is None:
            new_elements.append(_elements[idx])
    
    _elements = list(map(partial(RuntimeActionableElement, xpath_included=xpath_included), new_elements))
    # attributes = [element.get_all_attributes() for element in _elements]
    # _elements = [element for element in _elements if e_comparator.is_contain(element.to_actionable_element(),objectManager.get_by_tagname(element.get_attribute('tag_name'))) is None]
    # _elements = list(map(partial(RuntimeActionableElement, xpath_included=xpath_included), _elements))

    # _elements = list(map(partial(RuntimeActionableElement, xpath_included=xpath_included),driver.find_elements(by=By.XPATH, value=query_value)))
    # _elements = [e for e in _elements if e is not None and e.is_interactable() and e.is_attached()]
    # logger.debug(f'get interactable elements time : {time.time() - start}')
    return _elements

def is_form_child(el: RuntimeActionableElement):
    web_el = el._runtime_element
    curr_el: WebElement = web_el
    while (curr_el.tag_name != 'html'):
        curr_el = curr_el.find_element(by=By.XPATH, value="..")
        if curr_el.tag_name == 'form': return True
    return False

def get_anchors(driver, ObjectManager, xpath_included=True ):
    return get_actionable_elements(driver, ObjectManager, '//a', xpath_included)

def get_buttons(driver, ObjectManager, xpath_included=True ):
    return get_actionable_elements(driver, ObjectManager, '//button', xpath_included)

def get_inputs(driver, xpath_included=True):
    all_inputs = get_actionable_elements(driver, '//input')
    return filter(lambda e: not is_form_child(e), all_inputs)

def get_forms(driver, ObjectManager, xpath_included=True):
    return get_actionable_elements(driver, ObjectManager, '//form')

def extract_page_info(driver, objectManager: ObjectManager(), obj_getters=[get_anchors, get_buttons, get_forms], xpath_included=True) -> PageData:
    actionable_elements = []
    # for getter in obj_getters: actionable_elements += getter(driver, objectManager, xpath_included=xpath_included)
    logger.info(f"Number of Actionable Elements: {len(actionable_elements)}")
    return PageData(url=driver.current_url, 
                title=driver.title, 
                screenshot=None, 
                page_source = driver.page_source,
                actionable_elements=actionable_elements)

def save_screenshot(driver, save_path, filename="screenshot.png"):
    # get screenshot for the current web page
    image_path =  os.path.join(save_path, filename)
    s = driver.get_window_size()
    w = driver.execute_script('return document.body.parentNode.scrollWidth')
    h = driver.execute_script('return document.body.parentNode.scrollHeight')
    driver.set_window_size(w, h)
    driver.find_element(by=By.TAG_NAME, value="body").screenshot(image_path)
    driver.set_window_size(s['width'], s['height'])
    return image_path

def get_place(driver, objManager: ObjectManager, xpath_included=True) -> Place:
    pdata = extract_page_info(driver, xpath_included=xpath_included)
    serialized_objects, _ = objManager.push_objects(pdata.actionable_elements, save_to_disk=False)
    pdata.obj_uuids = [obj.get_attribute('uuid') for obj in serialized_objects]
    return  Place(randomword(16), data=pdata)
    
def obtain_action_elements_in_page(driver) -> List[ActionableElement]:
    pdata = extract_page_info(driver, xpath_included=False)
    return [e.to_actionable_element() for e in pdata.actionable_elements]