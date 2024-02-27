from re import I
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from element.exceptions import InvalidDataError
from selenium.webdriver.common.keys import Keys
from abc import ABC, abstractmethod
from loguru import logger
import json

JAVA_DECRYPT_DIR = "test_generator/JavaDecrypt"

class BaseAction(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def perform(self, driver, element, *args, **kwargs):
        pass

class ElementFreeAction(ABC):
    @property
    @abstractmethod
    def name(self):
        pass
    
    @abstractmethod
    def perform(self, driver, *args, **kwargs):
        return

class clickAction(BaseAction):
    @property
    def name(self):
        return "click"

    def perform(self, driver, element, *args, **kwargs):
        action_chains = ActionChains(driver)
        action_chains.click(element).perform()

class doubleClickAction(BaseAction):
    @property
    def name(self):
        return "doubleClick"

    def perform(self, driver, element, *args, **kwargs):
        action_chains = ActionChains(driver)
        action_chains.double_click(element).perform()

class sendKeysAction(BaseAction):
    @property
    def name(self):
        return "sendKeys"

    def perform(self, driver, element, *args, **kwargs):
        import re
        inputs = kwargs.get('data', None)
        if inputs == None:
            raise InvalidDataError('No provided KEY Press for this given action')
        action_chains = ActionChains(driver)
        key = re.findall(pattern="\((Keys.+)\)", string=inputs[0])[0]
        action_chains.click(element).send_keys(eval(key))
        action_chains.perform()

class acceptAlertAction(ElementFreeAction):
    def __init__(self) -> None:
        super().__init__()
    @property
    def name(self):
        return "acceptAlert"

    def perform(self, driver, *args, **kwargs):
        alert = Alert(driver=driver)
        try:
            alert.accept()
            return True
        except:
            return False
        
class switchToWindowIndexAction(ElementFreeAction):
    def __init__(self) -> None:
        super().__init__()
    
    @property
    def name(self):
        return "switchToWindowIndex"

    def perform(self, driver: webdriver.Chrome, *args, **kwargs):
        inputs = kwargs.get('data', None)
        if inputs == None:
            raise InvalidDataError(f'No provided input data for {self.name} action')
        index = int(inputs)
        try:
            driver.switch_to.window(driver.window_handles[index])
        except:
            return False
        return True

class switchToWindowUrlAction(ElementFreeAction):
    def __init__(self) -> None:
        super().__init__()
    
    @property
    def name(self):
        return "switchToWindowUrl"

    def perform(self, driver: webdriver.Chrome, *args, **kwargs):
        inputs = kwargs.get('data', None)
        if inputs == None:
            raise InvalidDataError(f'No provided input data for {self.name} action')
        url = inputs
        tabs = driver.window_handles
        
        for tab in tabs:
            driver.switch_to.window(tab)
            current_url = driver.current_url
            
            if current_url == url:
                return True
        
        return False

class switchToWindowTitleAction(ElementFreeAction):
    def __init__(self) -> None:
        super().__init__()
    
    @property
    def name(self):
        return "switchToWindowTitle"

    def perform(self, driver: webdriver.Chrome, *args, **kwargs):
        import time
        
        inputs = kwargs.get('data', None)
        if inputs == None:
            raise InvalidDataError(f'No provided input data for {self.name} action')
        title = inputs
        tabs = driver.window_handles
        
        for tab in tabs:
            driver.switch_to.window(tab)
            time.sleep(2)
            current_title = driver.title
            
            if current_title == title:
                return True
        
        return False

class setEncryptedText(BaseAction):
    @property
    def name(self):
        return "setEncryptedText"
    def perform(self, driver, element, *args, **kwargs):
        inputs = kwargs.get('data', None)
        if inputs == None:
            raise InvalidDataError('No provided data for this given action')
        if isinstance(inputs, list):
            data = inputs[0]
        else:
            data = inputs
        
        import os
        from subprocess import PIPE
        import subprocess
        import glob
        pwd = os.getcwd()
        os.chdir(JAVA_DECRYPT_DIR)
        if len(glob.glob('*.class')) == 0:
            logger.debug(f"Build file .java")
            p = subprocess.run(args=['make', 'build'], text=True, stderr=PIPE, stdout=PIPE)
            if p.returncode != 0:
                raise Exception(f"Encounter error: {p.stderr}")
        p = subprocess.run(args=['make', 'run', f'STR={data}'], text=True, stderr=PIPE, stdout=PIPE)
        os.chdir(pwd)
        logger.debug(f"Decrypting string: '{data}' -> '{p.stdout.strip()}'")
        if p.returncode != 0:
            raise Exception(f"Encounter error: {p.stderr}")

        input_data = p.stdout.strip()
        action_chains = ActionChains(driver)
        action_chains.click(element).send_keys(input_data).perform()

class setTextAction(BaseAction):
    @property
    def name(self):
        return "setText"

    def perform(self, driver, element, *args, **kwargs):
        inputs = kwargs.get('data', None)
        if inputs == None:
            raise InvalidDataError('No provided data for this given action')
        if isinstance(inputs, list):
            data = inputs[0] 
        else:
            data = inputs
        action_chains = ActionChains(driver)
        # action_chains.reset_actions()
        element.clear()
        action_chains.click(element).send_keys(data).perform()


class selectOptionByValueAction(BaseAction):
    @property
    def name(self):
        return "selectOptionByValue"

    def perform(self, driver, element, *args, **kwargs):
        inputs = kwargs.get('data', [])
        if len(inputs) != 2:
            raise InvalidDataError('Incorrect data format!')

        data = inputs[0]
        Select(element).select_by_value(data)

class selectOptionByVisibleTextAction(BaseAction):
    @property
    def name(self):
        return "selectOptionByVisibleText"

    def perform(self, driver, element, *args, **kwargs):
        inputs = kwargs.get('data', [])
        if len(inputs) != 2:
            raise InvalidDataError('Incorrect data format!')
        data = inputs[0]
        Select(element).select_by_visible_text(data)

class fillFormData(BaseAction):
    
    @property
    def name(self):
        return "fillFormData"
    
    def perform(self, driver, element, *args, **kwargs):
        from element.Element import RuntimeActionableElement
        with open('formData.json') as fp:
            config_data = json.load(fp).get(driver.current_url, None)
        
        if config_data is None:
            logger.error(f" formData for url~{driver.current_url} is not provided !")
            return False
        else:
            logger.info(f" formData for url~{driver.current_url} is: {config_data}")

        for child_el in map(RuntimeActionableElement, element.find_elements(By.XPATH, ".//input[@type='text' or @type='password']")):
            for attr in ['id', 'name']:
                if child_el.get_attribute(attr) in config_data.keys():
                    #child_el._runtime_element.clear()
                    logger.debug(f"found the child element: {child_el}, use the following value to fill in: {config_data[child_el.get_attribute(attr)]}")
                    is_succes = child_el.perform(driver, data=config_data[child_el.get_attribute(attr)])
                    logger.debug(f"fillingData -- done")
                    if is_succes: break
        
        try:
            submit_btn = driver.find_element(By.XPATH, config_data['submit_btn_xpath'])
            RuntimeActionableElement(submit_btn).perform(driver)
            return True
        except NoSuchElementException as e:
            return False

all_actions = {
    'switchToWindowIndex': switchToWindowIndexAction(),
    'switchToWindowUrl': switchToWindowUrlAction(),
    'switchToWindowTitle': switchToWindowTitleAction(),
    'acceptAlert': acceptAlertAction(),
}