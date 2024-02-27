from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from petrinet.PetriNet import ActionableTransition, Place, PetriNet
from element.Element import RuntimeActionableElement, ActionableElement
from repository.core import ObjectManager
from element.selectors.random_strategy import RandomStrategySelector
from element.operators import get_style, apply_style, highlight_element
from page.extractor import extract_page_info, save_screenshot, get_place
from backtrack import backtrack
from selenium.webdriver.chrome.service import Service
from callbacks import Callback, PetriNetBuilderCallback
from validations import Validation
from page.page import PageData
import sys
# from webdriver_manager.chrome import ChromeDriverManager
import time

sys.setrecursionlimit(1_000_000)
from urllib.parse import urlparse
from pathlib import Path
import datetime
import random
import crawler_logger
from loguru import logger


def timestamp():
    return int(time.time())

def traverse(driver,
             objManager: ObjectManager,
             callbacks: Callback = None,
             validators: list[Validation] = [],
             starting_place: list[Place] = [], max_depth=15) -> Place:
    logger.debug("Starting place: [{}]".format(starting_place))
    for callback in callbacks: callback.on_crawl_start(driver)
    for _ in range(max_depth):
        # callback.on_parse_html_start(driver)
        # validator.on_parse_html_start(driver)
        for callback, validator in zip(callbacks, validators):
            callback.on_parse_html_start(driver)
            validator.on_parse_html_start(driver)

        #----------------------------
        pdata: PageData = extract_page_info(driver)
        for callback, validator in zip(callbacks, validators):
            callback.on_parse_html_end(driver, pdata)
            validator.on_parse_html_end(driver, pdata)

        serialized_objects, _ = objManager.push_objects(pdata.actionable_elements)
        for callback in callbacks: callback.on_push_object_end(serialized_objects)

        candidate_masks = objManager.generate_mask(serialized_objects)
        for callback, validator in zip(callbacks, validators):
            callback.on_create_mask_end(candidate_masks)
            validator.on_create_mask_end(candidate_masks)

        pdata.object_uuids = ([obj.get_attribute('uuid') for obj in serialized_objects])
        pdata.candidate_masks = candidate_masks
        #----------------------------
        is_chosen = False
        num_retries = 0
        max_retries = int(pdata.num_objects / 3)

        for callback in callbacks: callback.on_select_action_start(serialized_objects, candidate_masks)
        while not is_chosen and num_retries <= max_retries:
            try:
                selected_idx = RandomStrategySelector(pdata.actionable_elements, candidate_masks).select()
                selected_element: RuntimeActionableElement = pdata.actionable_elements[selected_idx]
                for callback in callbacks:  callback.on_execute_action_start(driver, selected_element)
                if selected_element.perform(driver):
                    is_chosen = True
                    logger.info(" ↳ selected element: " + str(selected_element))
                for callback in callbacks: callback.on_execute_action_end(selected_element)

            except Exception as e:
                # logger.warning(f"[retry: #{num_retries}] Exception Error: \n" + str(e))
                num_retries += 1
                continue

        if num_retries > max_retries:
            raise Exception('num of selection times exceed max_retries')
        # ----------------------

        objManager.add_visited_object(serialized_objects[selected_idx])
        for callback in callbacks: callback.on_navigation_step_end(selected_element, pdata)

    logger.warning('exceed the max_depth, backtrack...')


def get_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(options=options)


def start(url, project_id=None):
    log_folder = crawler_logger.get_log_folder_name()
    # for WEB UI
    if project_id is not None:
        working_dir = crawler_logger.get_working_dir(project_id)
        crawler_logger.init_logger(project_id)
    else:
        working_dir = f"running_logs/{log_folder}"

    web_driver = get_driver()
    logger.debug(f'CRAWLING_START: {timestamp()}')
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
    
    

    try:
        while True:
            try:
                callback = PetriNetBuilderCallback(working_dir, petriNet, current_place)
                validator = Validation(base_domain)
                traverse(web_driver, objManager, [callback], [validator], current_place)
            except Exception as e:
                logger.info(str(e))

            logger.debug("Looking un explored object(s)...")
            # resume_place = random.choice(list(petriNet.place()))
            if not isinstance(resume_place, Place):
                unexplored_object_uuids = objManager.unexplored_objects
                target_uuid = None
                for place in sorted(petriNet.place(), key=lambda _: random.random()):
                    for uuid in place.data.object_uuids:
                        if uuid in unexplored_object_uuids:
                            resume_place = place
                            target_uuid = uuid
                            break
                    if isinstance(resume_place, Place): break
                logger.warning(f"found an unexplored object, with uuid={target_uuid}, in place={resume_place.name}")

            logger.debug("Start backtracking...")
            current_place = backtrack(web_driver, petriNet, objManager, resume_place)
    except Exception as e:
        logger.exception(f'Unexpected error. {e}')
    finally:
        web_driver.quit()
        logger.debug(f'CRAWLING_END: {timestamp()}')


if __name__ == "__main__":
    # driver = get_driver()
    # url = "http://localhost:3000/addressbook/index.php"
    # url = "http://localhost/phpfusion_v8/news.php"
    # url = "http://localhost:3000/ppma_052/index.php?r=entry/index"
    url = "http://phpfusion_v91000.loc/"

    # url = "http://localhost:4000/"
    # start(url, driver, "fg9TaMhKejqi7m1HUxHb")
    start(url)
