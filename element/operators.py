from cmd import IDENTCHARS
from functools import partial
from typing import Union
from xml.dom import NotFoundErr
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.ui import WebDriverWait

from element.Element import RuntimeActionableElement, ActionableElement
from loguru import logger

def find_element(serialized_element: ActionableElement, driver, trans_type: 'str'=None) -> Union[RuntimeActionableElement,None]:
    def v1():
        all_xpaths = ['absolute_xpath', 'robula_xpath', 'neighbor_xpath']
        for xpath in all_xpaths:
            xpath_value = serialized_element.get_attribute(xpath)
            # assert xpath_value is not None
            if xpath_value is None: continue 
            el = driver.find_elements(by=By.XPATH, value=xpath_value)
            # delay = 3
            # el = WebDriverWait(driver=driver, timeout=delay).until(
            #     EC.presence_of_element_located((By.XPATH, xpath))
            # )
            if len(el) > 0: return RuntimeActionableElement(el[0])
        return None
    def v2():
        for n, xpaths in serialized_element.get_attribute('selectors')['xpath'].items():
            if n == 'any':
                continue
            for xpath in xpaths:
                try:
                    if trans_type is None:
                        logger.debug(f"Use XPATH {xpath} to find element")
                    else:
                        logger.debug(f"Use XPATH {xpath} to find element for {trans_type} action")
                    # el = driver.find_element(by=By.XPATH, value=xpath)
                    delay = 3
                    el = WebDriverWait(driver=driver, timeout=delay).until(
                        EC.presence_of_element_located((By.XPATH, xpath))
                    )
                    if el is not None: return RuntimeActionableElement(el)
                except Exception as e:
                    logger.info(f"Can not use XPATH {xpath} to find element")
        return None
    if serialized_element.get_attribute('absolute_xpath') != None:
        return v1()
    else:
        return v2()

def get_supported_actions(el: Union[WebElement, dict]) -> list[str]:
    if isinstance(el, WebElement):
        tag_name = el.tag_name
        e_type = el.get_attribute('type') 
    elif isinstance(el, dict):
        tag_name = el.get('tag_name')
        e_type = el.get('type')

    if tag_name in ['button', 'a']:
        return ['click', ]
    elif tag_name in ['input', 'textarea']:
        return ['click'] if e_type in ['button', 'checkbox', 'submit'] else ['setText']
    elif tag_name == 'form':
        return ['fillFormData']
    elif tag_name == 'select':
        return ['selectOptionByVisibleTextAction', 'selectOptionByValue', 'selectOptionByLabel'] # TODO: add default supported actions for select
    else:
        return ['click', ]     

def apply_style(element, new_style):
    driver = element._parent
    driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element, new_style)

def get_style(element):
    return  element.get_attribute('style')

def highlight_element(element): 
    apply_style(element, new_style="background: yellow; border: 2px solid red;")
