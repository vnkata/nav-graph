from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from typing import Union

from petrinet.PetriNet import ActionableTransition, Place, PetriNet, Transition, Arc
from element.Actions import (
    ElementFreeAction,
    all_actions
)
from element.Element import RuntimeActionableElement, ActionableElement, AnchorLinkElement
from repository.core import ObjectManager
from element.selectors.random_strategy import RandomStrategySelector
from element.operators import get_style, apply_style, highlight_element
from page.extractor import extract_page_info, save_screenshot, get_place
from petrinet.traversal_utils import generate_path
from backtrack import backtrack
from selenium.webdriver.chrome.service import Service
from callbacks import Callback, PetriNetBuilderCallback
from validations import Validation
from page.page import PageData
from petrinet import PetriNetConverter as pnc
from test_generator.StateGraph.PetriNet import CustomPetriNet
from petrinet.PetriNetConverter import parse_obj_repo_path, make_trans_from_step_info
from selenium.webdriver.common.by import By
import sys
from functools import partial

from webdriver_manager.chrome import ChromeDriverManager
import time

from element.operators import find_element
import copy


sys.setrecursionlimit(1_000_000)
from urllib.parse import urlparse
from pathlib import Path
import datetime
import random
import crawler_logger
from loguru import logger
import os
from argparse import ArgumentParser
import argparse
import textwrap

pareser = ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter
)
pareser.add_argument(
    '-p', '--project',
    help="""\
        Assign path of your project (record test case use Katalon).
            + ex: --project '/Users/user/Katalon Studio/Test'
    """,
    default=None
)
pareser.add_argument(
    '-u', '--url', 
    help=
    """
        Specify URL of page you want to crawl. Otherwise it will use default URL of your test case.
            + Ex: --url 'helloworld.com'
    """,
    default=None,
)
pareser.add_argument(
    '-tc', '--testcase',
    default=None,
    action='append',
    help=
    """
        Specify name of test cases you want to spare and crawl. Otherwise it will parse all test cases included in your project.
            + Ex: --testcase 'test 1' --testcase 'test 2'
    """
)


def timestamp():
    return int(time.time())

def scroll_element_center(driver:webdriver.Chrome, element:RuntimeActionableElement, delay_secs=1):
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
    

def traverse(url: 'str',
             web_driver,
             objManager: ObjectManager,
             trajectory,
             working_dir = "",
             petriNet: PetriNet = None) -> Place:
    current_place: Place = None
    for r in petriNet.root:
        if r.name == trajectory.places[0].name:
            current_place = r
            break
    
    if url is None:
        url = current_place.data['current_url']
    logger.info(f"Query to URL {url}")
    web_driver.get(url)
    
    test_step = 1
    
    if len(trajectory.transitions) == 0:
        logger.debug (f"no transition in the trajectory!, return root place~({str(petriNet.root)})")
        return petriNet.root[0]
    
    for step in range(len(trajectory.places)):
        place_name = current_place.name
    
        save_dir = os.path.join(working_dir, "places", place_name)
        Path(save_dir).mkdir(parents=True, exist_ok=True)
        
        logger.info(f"{70*'='}")
        logger.info(f"{20*'>'} Test step {test_step} {20*'<'}")
        logger.info("Page has loaded completely")
        
        # start_time = time.time()
        # pdata: PageData = extract_page_info(web_driver)
        # logger.info(f"Total of time for extract all action elements in current place {current_place.name}: {time.time() - start_time}")
        # pdata.screenshot = save_screenshot(web_driver, save_dir)
        # serialized_objects, _ = objManager.push_objects(pdata.actionable_elements)
        
        # candidate_masks = objManager.generate_mask(serialized_objects)
        # pdata.candidate_masks = candidate_masks
        # pdata.object_uuids = ([obj.get_attribute('uuid') for obj in serialized_objects])
        
        # pdata.export(filename=os.path.join(save_dir, "info.json"))
        
        # candidate_transitions = []
        # for x in current_place.output_arc():
        #     if x.destination.name == trajectory.transitions[step].name:
        #         candidate_transitions.append(x.destination)
        
        # next_transition: Transition = candidate_transitions[0]
        # next_element: ActionableElement = next_transition.data
        # if len(next_transition.output_arc()) == 0:
        #     logger.debug(f"transition~({next_transition}) does not contain any output_arc()")
        #     return current_place

        # next_action_rt = None
        
        # input_data = list(next_transition.output_arc())[0].data
        
        # if next_element is None and 'Alert' in next_transition.transition_type:
        #     next_action_rt: ElementFreeAction = all_actions[next_transition.transition_type]

        #     logger.debug(f"Input data for action {next_transition.transition_type} is {input_data}")
        #     if not next_action_rt.perform(web_driver, data=input_data):
        #         logger.debug(f"unable to perform action (selected: {next_action_rt})")
        #         return current_place
        #     else:
        #         logger.debug(f"perform action successful (selected:{next_action_rt})")
        #     continue
        
        candidate_transitions = []
        for x in current_place.output_arc():
            if x.destination.name == trajectory.transitions[step].name:
                candidate_transitions.append(x.destination)
        
        next_transition: Transition = candidate_transitions[0]
        next_element: ActionableElement = next_transition.data
        if len(next_transition.output_arc()) == 0:
            logger.debug(f"transition~({next_transition}) does not contain any output_arc()")
            return current_place
        
        next_action_rt = None
        
        input_data = list(next_transition.output_arc())[0].data
        if next_element is None and next_transition.transition_type in all_actions.keys():
            next_action_rt: ElementFreeAction = all_actions[next_transition.transition_type]
            # next_action_rt.perform(driver=web_driver, data=input_data)
        else:
            next_action_rt: RuntimeActionableElement = find_element(next_element, web_driver, next_transition.transition_type) 
            if next_action_rt is None:
                logger.debug(f"element~({next_element}) can not found!")
                return current_place
            
            start_time = time.time()
            pdata: PageData = extract_page_info(web_driver, objManager, xpath_included=True)
            logger.info(f"Total of time for extract all action elements in current place {current_place.name}: {time.time() - start_time}")
            pdata.screenshot = save_screenshot(web_driver, save_dir)
            serialized_objects, _ = objManager.push_objects(pdata.actionable_elements)
            
            candidate_masks = objManager.generate_mask(serialized_objects)
            pdata.candidate_masks = candidate_masks
            pdata.object_uuids = ([obj.get_attribute('uuid') for obj in serialized_objects])
            
            pdata.export(filename=os.path.join(save_dir, "info.json"))

            next_action_rt.update_action(next_transition.transition_type)
            scroll_element_center(driver=web_driver, element=next_action_rt, delay_secs=0.5)
            
            visited_object = objManager.push_object(next_action_rt)
            objManager.add_visited_object(visited_object)
            next_element.assign_uuid(value=visited_object.get_attribute('uuid'))
            
            next_action_rt._element.generate_xpath_attributes(next_action_rt._runtime_element, web_driver)
            original_style = get_style(next_action_rt._runtime_element)
            highlight_element(next_action_rt._runtime_element)
            
            selected_element_screenshot = save_screenshot(
                web_driver,
                save_path=os.path.join(working_dir, "screenshots"),
                filename=visited_object.get_attribute('uuid') + ".png"
            )
            
            next_element._all_attributes['screenshot'] = selected_element_screenshot
            current_place.data = pdata
            
            if next_action_rt.is_attached():
                apply_style(next_action_rt._runtime_element, original_style)
        
        logger.debug(f"Input data for action {next_transition.transition_type} is {input_data}")
        if not next_action_rt.perform(web_driver, data=input_data):
            logger.debug(f"unable to perform action (selected: {next_action_rt})")
            return current_place
        else:
            logger.debug(f"perform action successful (selected:{next_action_rt})")
        
        next_place = [pl.destination for pl in next_transition.output_arc() if pl.destination.name == trajectory.places[step+1].name][0]
        current_place =  next_place
        
        test_step += 1


def get_driver():
    options = Options()
    dc = DesiredCapabilities().CHROME
    dc["pageLoadStrategy"] = "normal"
    # options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(desired_capabilities=dc, options=options, executable_path=ChromeDriverManager().install())


def start(url: 'str', petriNets: dict, project_id=None):
    log_folder = crawler_logger.get_log_folder_name()
    # for WEB UI
    if project_id is not None:
        working_dir = crawler_logger.get_working_dir(project_id)
        crawler_logger.init_logger(project_id)
    else:
        working_dir = f"running_logs/{log_folder}"

    logger.debug(f'CRAWLING_START: {timestamp()}')
    # base_domain = urlparse(url).netloc
    Path(working_dir + "/places").mkdir(parents=True, exist_ok=True)
    Path(working_dir + "/screenshots").mkdir(parents=True, exist_ok=True)

    objManager = ObjectManager(working_dir=working_dir)
    logger.add(f"{working_dir}/crawling.log", backtrace=True, diagnose=True)

    for case_name, petriNet in petriNets.items():
        web_driver = get_driver()
        trajectory = generate_path(petriNet=petriNet)
        logger.debug(f"Start traverse for test case: {case_name}")
        try:
            logger.info(f"Length of test case: {len(trajectory.transitions)}")
            traverse(url, web_driver, objManager, trajectory, working_dir, petriNet)

        except Exception as e:
            logger.exception(f'Unexpected error. {e}')
            web_driver.quit()
    
    web_driver.quit()
    allNets = list(petriNets.values())
    baseNet = allNets[0]
    if len(petriNets) > 1:
        for targNet in allNets[1:]:
            baseNet = PetriNet.merge(ptnBase=baseNet, ptnTarget=targNet)
    # new_net.merge_places(object_manager=objManager)
    PetriNet.save(baseNet, f"{working_dir}/petri-net.pkl")
    logger.debug(f'CRAWLING_END: {timestamp()}')


if __name__ == "__main__":
    pnc.SCRIPT_INPUT_DIR = "test_generator/GroovyParser/Data"
    pnc.SCRIPT_OUTPUT_DIR = "test_generator/GroovyParser/Output"
    pnc.GROOVY_PARSER_DIR = "test_generator/GroovyParser"
    
    args = pareser.parse_args()
    
    proj = args.project
    proj = "/Users/luong.nguyen/Katalon Studio/Web UI Tests Project (Shopping Cart)"
    if proj is None:
        raise Exception("You have not specified path for project yet!")
    
    testcases = pnc.fetch_script_paths(proj)
    
    nets = []
    script_lists = []
    # NOTE: change to run only this test case
    selected_testcases = args.testcase
    selected_testcases = ['content_categories']
    if selected_testcases is None or len(selected_testcases) == 0:
        selected_testcases = testcases.keys()
    
    for case, script_list in testcases.items():
        if case in selected_testcases:
            net, scripts = pnc.construct_code_based_petrinet_(proj, (case, script_list))
            
            nets.append(net)
            script_lists.append(script_list)

    new_nets = {}
    
    for case_name, net, scripts in zip(selected_testcases, nets, script_lists):
        try:
            new_net = pnc.codeBased_to_actionBased(proj, net, scripts)
            new_nets[case_name] = new_net
        except:
            logger.exception(f"Unexpected Error with test case: {case_name}")
    
    url = "http://localhost/joomla400/administrator/index.php"
    
    if len(new_nets.items()) == 0:
        raise Exception("Your parsed test cases list is empty!")
    
    start(url, new_nets)
