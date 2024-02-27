import chromedriver_binary
import sqlite3

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from element.Element import all_actions
from element.Actions import clickAction
from element.Element import RuntimeActionableElement

from petrinet.PetriNet import ActionableTransition, Place, PetriNet
from repository.core import ObjectManager
from page.extractor import extract_page_info
from callbacks import Callback, UserTrackingPetriNetBuilderCallback
from validations import Validation
from page.page import PageData
import sys
import time

from urllib.parse import urlparse
from pathlib import Path
import crawler_logger
from loguru import logger
sys.setrecursionlimit(1_000_000)


def parse(driver,
             objManager: ObjectManager,
             callbacks: Callback = None,
             validators: list[Validation] = [],
             starting_place: list[Place] = [],
             all_steps: list[dict]=[]) -> Place:
    logger.debug("Starting place: [{}]".format(starting_place))
    for callback in callbacks: callback.on_crawl_start(driver)

    for idx, step in enumerate(all_steps):
        action, target_selector = step['event'], step['target_selector']
        value, xpath = step['target_attributes_value'], step['target_attributes_text']

        # if driver.current_url.startswith("http://phpfusion_v90310.loc/administration/index.php"):
        # if idx == len(all_steps) - 5:
        #     driver.get("http://phpfusion_v90310.loc/administration/file_manager.php")
        for callback, validator in zip(callbacks, validators):
            callback.on_parse_html_start(driver)
            validator.on_parse_html_start(driver)

        #----------------------------
        pdata: PageData = extract_page_info(driver, obj_getters=[])
        for callback, validator in zip(callbacks, validators):
            # callback.on_parse_html_end(driver, pdata)
            # validator.on_parse_html_end(driver, pdata)
            pass

        serialized_objects, _ = objManager.push_objects(pdata.actionable_elements)
        # for callback in callbacks: callback.on_push_object_end(serialized_objects)
        # candidate_masks = objManager.generate_mask(serialized_objects)
        # for callback, validator in zip(callbacks, validators):
        #     callback.on_create_mask_end(candidate_masks)
        #     validator.on_create_mask_end(candidate_masks)

        pdata.object_uuids = {obj.get_attribute('uuid'): None for obj in serialized_objects}
        # pdata.candidate_masks = candidate_masks
        # for callback in callbacks: callback.on_select_action_start(serialized_objects, candidate_masks)

        if action == "click":
            if step['target_selector'] in ['button', 'input', 'a']:
                element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, xpath)))
                selected_element = RuntimeActionableElement(driver.find_element(By.XPATH, xpath) , driver)
                objManager.push_objects([selected_element])
                for callback in callbacks:  callback.on_execute_action_start(driver, selected_element)
                element.click()
            if step['target_selector'] == 'select':
                element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, xpath)))
                selected_element = RuntimeActionableElement(element , driver)
                selected_element.update_action(action_name="selectOptionByValue")
                objManager.push_objects([selected_element])
                for callback in callbacks:  callback.on_execute_action_start(driver, selected_element)
                #element.click()
                selected_element.perform(data=value)


        elif action == "form" and target_selector != "form":
            # update action name to be consistent with our name convention.
            action = "setText"
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath)))
            selected_element = RuntimeActionableElement(driver.find_element(By.XPATH, xpath) , driver)
            objManager.push_objects([selected_element])
            for callback in callbacks:  callback.on_execute_action_start(driver, selected_element)
            try:
                element.clear()
            except Exception as e:
                #logger.debug (str(e))
                pass
            
            logger.info(f"Data={value}")
            element.send_keys(value)
        else:
            continue
        # ----------------------
        for callback in callbacks:  callback.on_execute_action_end( selected_element)
        objManager.add_visited_object(selected_element.to_actionable_element())
        selected_element._action = all_actions.get(action, clickAction )()
        for callback in callbacks: callback.on_navigation_step_end(selected_element, pdata, arc_data=[value])

def get_driver():
    options = Options()
    # options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(options=options)


def start(url, project_id=None):
    log_folder = crawler_logger.get_log_folder_name()
    if project_id is not None:
        working_dir = crawler_logger.get_working_dir(project_id)
        crawler_logger.init_logger(project_id)
    else:
        working_dir = f"running_logs/{log_folder}"

    web_driver = get_driver()
    logger.debug(f'CRAWLING_START: {int(time.time())}')
    base_domain = urlparse(url).netloc
    Path(working_dir + "/places").mkdir(parents=True, exist_ok=True)
    Path(working_dir + "/screenshots").mkdir(parents=True, exist_ok=True)

    petriNet = PetriNet()
    objManager = ObjectManager(working_dir=working_dir)
    current_place: Place = None
    logger.add(f"{working_dir}/crawling.log", backtrace=True, diagnose=True)

    if len(petriNet.node()) == 0:
        logger.debug('Current Petri-Net graph is empty, load the initial url first.')
        web_driver.get(url)
    
    callback = UserTrackingPetriNetBuilderCallback(working_dir, petriNet, current_place)
    validator = Validation(base_domain)


    # ---------------------
    # Get user tracking steps.
    connection = sqlite3.connect("event_db.db", check_same_thread=False)
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events ")
    all_steps = cursor.fetchall()

    def remove_duplicate_steps(all_steps):
        outputs = []
        cmp_attrs = ['event', 'target_selector', 'target_attributes_text', 
        'target_attributes_name', 'target_attributes_id']
        for idx, step in enumerate(all_steps):
            step = dict(step)
            precheck = True
            if idx + 1 < len(all_steps): 
                for iid in cmp_attrs:
                    if step[iid] != all_steps[idx+1][iid]:
                        precheck = False
                if idx == 0 and step['target_attributes_value'] == None: 
                    outputs.append(step)
                    continue
                if  all_steps[idx+1]['target_attributes_value'] == None:
                    outputs.append(step)
                    continue

                if precheck and all_steps[idx+1]['target_attributes_value'].startswith(step['target_attributes_value']):
                    continue
            outputs.append(step)
        return outputs

    all_steps = remove_duplicate_steps(all_steps)
    # ---------------------

    parse(web_driver, objManager, [callback], [validator], current_place, all_steps)
    web_driver.quit()


start("http://phpfusion_v90310.loc/")










