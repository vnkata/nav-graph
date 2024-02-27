from mailbox import NotEmptyError
from typing import Union
from xml.dom import NotFoundErr
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
import selenium.common.exceptions as selenium_exceptions
from abc import ABC, abstractmethod
from xpath_locators.absolute import get_absolute_xpath
from xpath_locators.RobulaPlus import get_robula_xpath
from xpath_locators.NeighborXPath import get_neighbor_xpath

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from loguru import logger
import time
import json
from loguru import logger
from element.Actions import (
    BaseAction,
    clickAction,
    selectOptionByValueAction,
    selectOptionByVisibleTextAction,
    setTextAction,
    fillFormData,
    setEncryptedText,
    sendKeysAction,
    doubleClickAction
    # SendKeysAction,
    # DoubleClickAction,
    # ContextClickAction,
    # KeyUpAction,
    # KeyDownAction,
    # AutomaticFormFillingAction
)

all_actions = {
    'doubleClick': doubleClickAction,
    'click': clickAction, 
    'setText': setTextAction, 
    'setEncryptedText': setEncryptedText,
    # 'auto_form_filling': AutomaticFormFillingAction, 
    'fillFormData': fillFormData,
    'selectOptionByValue': selectOptionByValueAction, 
    'selectOptionByVisibleTextAction': selectOptionByVisibleTextAction, 
    'sendKeys': sendKeysAction
}

xpath_methods = {
    'absolute_xpath': get_absolute_xpath,
    # 'robula_xpath': get_robula_xpath,
    # 'neighbor_xpath': get_neighbor_xpath
}

buitin_selenium_attrs = {
            'properties': ['tag_name', 'text', 'size', 'rect', 'location', 'accessible_name', ],
            'functions': ['is_selected', 'is_enabled', 'is_displayed'],
            'attrs': ['innerHTML', 'outerHTML','innerText', 'id', 'class', 'type', 'style']
        }
replace_empty_to_none = lambda x: None if x == "" else x

def scroll_element_center(driver:webdriver.Chrome, element, delay_secs=1):
    """ Scroll browser to element with element is in the center of the browser

    Args:
        driver (webdriver.Chrome): web driver
        element (RuntimeActionableElement): element we need to execute
        delay_secs (int, optional): number of second we need to delay. Defaults to 1.

    Returns:
        None: 
    """
    size = element.get_attribute('size')
    location = element.get_attribute('location')
    
    desired_y = (size['height'] / 2) + location['y']
    window_h = driver.execute_script('return window.innerHeight')
    window_y = driver.execute_script('return window.pageYOffset')
    current_y = (window_h / 2) + window_y
    scroll_y_by = desired_y - current_y

    driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)
    time.sleep(delay_secs)

class Element(object):
    def __init__(self, init_attrs_data: dict={}):
        self._all_attributes = init_attrs_data
    
    def update_common_attributes_from_selenium(self, element: WebElement, xpath_included=False) -> bool:
        try:
            attributes = {att: getattr(element, att, None) for att in buitin_selenium_attrs['properties']} |\
                    {att: getattr(element, att)() for att in buitin_selenium_attrs['functions']} |\
                    {att: replace_empty_to_none(element.get_attribute(att)) for att in buitin_selenium_attrs['attrs']}

            self._all_attributes = self._all_attributes | attributes
            return True

        except selenium_exceptions.StaleElementReferenceException as e:
            print ('[update_common_attributes_from_selenium] ', e)
            return False

        except Exception as e:
            print ('[extract_attributes]', e)
            return False

    def update_attributes(self, element: WebElement, attrs:dict[str]) -> bool:
        added_attrs = {}
        for attr in attrs: added_attrs[attr] = replace_empty_to_none(element.get_attribute(attr))
        self._all_attributes = self._all_attributes | added_attrs
        return True
    
    def update_attributes_from_dict(self, data:dict) -> bool:
        self._all_attributes = self._all_attributes | data
        return True

    def generate_xpath_attributes(self, element: WebElement, driver, target_methods:list[str] = ['absolute_xpath']):
        xpath_d = {}
        for method in target_methods:
            if method not in self._all_attributes:
                try:
                    xpath_d[method] = xpath_methods[method](element, driver)
                except selenium_exceptions.StaleElementReferenceException as e:
                    logger.warning(str(e))
                    xpath_d[method] = "__error__"
                except Exception as e:
                    logger.warning(method+ " " + str(e))
                    xpath_d[method] = "__error__"

        self._all_attributes = self._all_attributes | xpath_d
        return True

    def get_attribute(self, attr, default=None) -> str:
        return self._all_attributes.get(attr, default)
    
    def __str__(self):
        return "%s_%s_%s_%s_%s" % (self.get_attribute('tag_name'), 
            self.get_attribute('accessible_name'),
            self.get_attribute('uuid'),
            self.get_attribute('id'),
            self.get_attribute('name')
        )
        # return str({'tag_name': self.get_attribute('tag_name'), 
        #             'visible_name': self.get_attribute('accessible_name'),
        #             'uuid': self.get_attribute('uuid')})
    
    def serializer(self):
        return self._all_attributes

    @property
    def json(self):
        return self.serializer()

class ActionableElement(Element):
    def __init__(self, comparable_attrs=[], supported_actions=["click", ], ):
        super().__init__()
        
        self._supported_actions = supported_actions
        self._comparable_attrs = comparable_attrs
    
    def assign_uuid(self, value, key='uuid'):
        self._all_attributes = self._all_attributes | {key: value}

    def __eq__(self, obj: object) -> bool:
        if obj is None:
            return False
        

        if True not in [isinstance(obj, ActionableElement), isinstance(obj, RuntimeActionableElement)]:
            logger.debug("obj_type: " + str(type(obj)))
            raise NotImplemented(f'Unknown object {obj} with type: {type(obj)}')
        
        if ((self.get_attribute('from_test_case') == True and self.get_attribute('is_augmented') == False) or
            (obj.get_attribute('from_test_case') == True and obj.get_attribute('is_augmented') == False)):
            return False
        
        if len(self._comparable_attrs) == 0:
            raise NotEmptyError('Comparable attributes need to be specified.')
        
        if isinstance(obj, RuntimeActionableElement):
            obj = obj.to_actionable_element()
        
        # Ref: obj_repo.generate_mask
        if obj.get_attribute('tag_name') != self.get_attribute('tag_name'): 
            return False
        
        for att in self._comparable_attrs: 
            if self.get_attribute(att) != obj.get_attribute(att):
                return False
        return True

    def __ne__(self, obj):
        return not self == obj

class ButtonElement(ActionableElement):
    def __init__(self, supported_actions=['click', ]):
        self._comparable_attrs = ['id', 'class', 'form', 'value', 'type' ] 
        super().__init__(self._comparable_attrs, supported_actions)

    def __eq__(self, obj: object) -> bool:
        # more advanced, strict comparisons will be defined here !
        return super().__eq__(obj)

class AnchorLinkElement(ActionableElement):
    def __init__(self, supported_actions=['click', ]):
        self._comparable_attrs = ['id', 'href', 'title', 'innerText',]
        super().__init__(self._comparable_attrs, supported_actions)


    def __eq__(self, obj: object) -> bool:
        # more advanced, strict comparisons will be defined here !
        return super().__eq__(obj)


class InputElement(ActionableElement):
    def __init__(self, supported_actions=['click', 'send_keys']):
        self._comparable_attrs = ['type', 'id', 'name', 'value', 'class', 'innerText']
        super().__init__(self._comparable_attrs, supported_actions)


    def __eq__(self, obj: object) -> bool:
        # more advanced, strict comparisons will be defined here !
        return super().__eq__(obj)

class TextAreaElement(ActionableElement):
    def __init__(self, supported_actions=['click', 'send_keys']):
        self._comparable_attrs = ['type', 'id', 'name', 'value', 'class', 'innerText']
        super().__init__(self._comparable_attrs, supported_actions)


    def __eq__(self, obj: object) -> bool:
        # more advanced, strict comparisons will be defined here !
        return super().__eq__(obj)

class FormElement(ActionableElement):
    def __init__(self,  supported_actions=["send_keys"]):
        self._comparable_attrs = ['type', 'id', 'name', 'value', 'class', 'innerText']
        super().__init__(self._comparable_attrs, supported_actions)

class SelectionElement(ActionableElement):
    # TODO: update selection element supported actions
    def __init__(self,  supported_actions=["selectOptionByValue", "selectOptionByLabel"]):
        self._comparable_attrs = ['type', 'id', 'name', 'class']
        super().__init__(self._comparable_attrs, supported_actions)

class ElementFactory:
    def __init__(self):
        self.cls_mapping = {
            'a': AnchorLinkElement,
            'button': ButtonElement,
            'input': InputElement,
            'textarea': TextAreaElement,
            'form': FormElement,
            'select': SelectionElement
        }   
    
    def from_webelement(self, element: WebElement, xpath_included=True, *args, **kwargs) -> ActionableElement:
        try:
            from element.operators import get_supported_actions
            el = self.cls_mapping.get(element.tag_name, ActionableElement)(supported_actions=get_supported_actions(element))
            # TODO: Will update later
            if element.is_enabled(): 
                res_1 = el.update_common_attributes_from_selenium(element)
                res_2 = el.update_attributes(element, el._comparable_attrs)
                if xpath_included:
                    _ = el.generate_xpath_attributes(element, element.parent, target_methods=['absolute_xpath'])
                if False in (res_1, res_2): return None 
                else: return el
            else:
                # logger.error("Element is not enabled!")
                return None

        except selenium_exceptions.StaleElementReferenceException as e:
            # logger.error(str(e))
            return None

    def from_dict(self, data: dict) -> ActionableElement:
        cls = self.cls_mapping.get(data['tag_name'], ActionableElement)
            
        # TODO: Need to update `supported actions` here
        from element.operators import get_supported_actions
        out = cls(supported_actions=get_supported_actions(data))
        out.update_attributes_from_dict(data)
        return out
    
    def get(self, obj: Union[WebElement, dict], xpath_included=True) -> ActionableElement:
        if isinstance(obj, WebElement): 
            return self.from_webelement(obj, xpath_included)
        elif isinstance(obj, dict):
            return self.from_dict(obj)

class RuntimeActionableElement(object):
    def __init__ (self, element: Union[WebElement, ActionableElement], driver=None, xpath_included=True):
        if isinstance(element, ActionableElement):
            assert driver is not None
            assert element is not None
            self._element = element
            from element.operators import find_element
            self._runtime_element = find_element(element, driver) # TODO: Inconsistent....

        elif isinstance(element, WebElement):
            self._element: ActionableElement = ElementFactory().get(element, xpath_included=xpath_included)
            self._runtime_element = element
        else:
            logger.error('Unknow element of type: ' + str(type(element)))
            return None

        if self._element is None: return None
        # self._action = None
        self._action = all_actions.get(self._element._supported_actions[0])()


    @property
    def json(self):
        return self._element.json
    
    def get_attribute(self, attr, default_value=''):
        return self._element.get_attribute(attr, default_value)

    def assign_uuid(self, value, key='uuid'):
        self._element.assign_uuid(value, key)
    
    def update_action(self, action_name):
        action_cls = all_actions.get(action_name, None)
        if action_cls is None:
            logger.error("action_cls can not be None")
            return
        self._action = action_cls()

    @property
    def supported_actions(self):
        return self._element._supported_actions

    @property
    def action(self):
        return self._action
    
    @action.setter
    def action(self, action: BaseAction):
        if action.name not in self._element._supported_actions:
            raise ValueError(f"Element does not have {action.name} event handler.")
        self._action = action

    def is_interactable(self):
        try:
            return self._element is not None and self._runtime_element.is_enabled()
        except selenium_exceptions.StaleElementReferenceException as e:
            return False
    
    def is_attached(self):
        return self.is_interactable()

    def perform(self, driver, *args, **kwargs):
        # A simple implement of wait mechanism, Selenium wait does not work in this case
        # TODO: Find another alternative to implement this `wait` mechanism 
        max_retries = 10
        for idx in range(max_retries):
            if not self.is_attached(): 
                logger.error(f"This selected element is not attached anymore")
                time.sleep(1)
                if idx == max_retries-1: return False
            else:
                break
        try:
            if self._action is None:
                from element.operators import get_supported_actions
                actions = get_supported_actions(self._runtime_element)
                self._action = all_actions.get(actions[0])()
            self._action.perform(driver, self._runtime_element, *args, **kwargs)
        except selenium_exceptions.MoveTargetOutOfBoundsException:
            scroll_element_center(driver=driver, element=self, delay_secs=1)
        except Exception as e:
            logger.error(f"Can not perfom action in this element {e}")
            return False
        return True

        # wait = WebDriverWait(driver, 10)
        # try:
        #     _ = wait.until(EC.element_to_be_clickable((By.XPATH, self.get_attribute('neighbor_xpath'))))
        #     self._action.perform(driver, self._runtime_element, *args, **kwargs)
        #     return True
        # except TimeoutException as e:
        #     logger.error(f"Can not perfom action in this element {e}")
        #     return False

    def to_actionable_element(self):
        out = self._element 
        return out
    
    def serializer(self):
        return self._element.serializer()
    
    def __str__(self):
        return self._element.__str__()

if __name__ == "__main__":
    pass