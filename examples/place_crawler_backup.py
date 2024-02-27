from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from typing import List, Union
from petrinet.PetriNet import ActionableTransition, Place, PetriNet, Transition, Arc
from element.Element import RuntimeActionableElement, ActionableElement, AnchorLinkElement
from repository.core import ObjectManager
from element.selectors.random_strategy import RandomStrategySelector
from element.operators import get_style, apply_style, highlight_element
from page.extractor import extract_page_info, save_screenshot, get_place
from petrinet.traversal_utils import select_path, create_trajectory
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
# from webdriver_manager.chrome import ChromeDriverManager
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
import uuid as uuid_m
import pickle
from subprocess import Popen, PIPE

def timestamp():
    return int(time.time())

def page_has_loaded(driver):
    page_sate = driver.execute_script('return document.readyState;')
    return page_sate == "complete"

def traverse(web_driver,
             objManager: ObjectManager,
             trajectory = None,
             working_dir = "",
             petriNet: PetriNet = None) -> Place:
    current_place: Place = None
    for r in petriNet.root:
        if r.name == trajectory.places[0].name:
            current_place = r
            break
    url = current_place.data['current_url']
    logger.info(f"Get URL {url}")
    web_driver.get(url)
    
    test_step = 1
    
    if len(trajectory.transitions) == 0:
        logger.debug (f"no transition in the trajectory!, return root place~({str(petriNet.root)})")
        return petriNet.root[0]
    
    for step in range(len(trajectory.places)):
        place_name = current_place.name
    
        save_dir = os.path.join(working_dir, "places", place_name)
        Path(save_dir).mkdir(parents=True, exist_ok=True)
        
        pdata: PageData = extract_page_info(web_driver)
        pdata.screenshot = save_screenshot(web_driver, save_dir)
        serialized_objects, _ = objManager.push_objects(pdata.actionable_elements)
        
        candidate_masks = objManager.generate_mask(serialized_objects)
        pdata.candidate_masks = candidate_masks
        pdata.object_uuids = ([obj.get_attribute('uuid') for obj in serialized_objects])
        
        # pdata.export(filename=os.path.join(save_dir, "info.json"))
        if page_has_loaded(web_driver) == False:               
            logger.info("Page has not loaded completely")
            while not page_has_loaded(web_driver):
                time.sleep(1)
        logger.info("Page has loaded completely")
        
        candidate_transitions = []
        for x in current_place.output_arc():
            if x.destination.name == trajectory.transitions[step].name:
                candidate_transitions.append(x.destination)
        
        next_transition: Transition = candidate_transitions[0]
        next_element: ActionableElement = next_transition.data
        if len(next_transition.output_arc()) == 0:
            logger.debug(f"transition~({next_transition}) does not contain any output_arc()")
            return current_place
        
        next_element_rt: RuntimeActionableElement = find_element(next_element, web_driver, next_transition.transition_type) 
        if next_element_rt is None:
            logger.debug(f"element~({next_element}) can not found!")
            return current_place
        
        next_element_rt.update_action(next_transition.transition_type)
        
        visited_object, is_visited = objManager.push_object(next_element_rt)
        if not is_visited:
            objManager.add_visited_object(visited_object)
        
        next_element_rt._element.generate_xpath_attributes(next_element_rt._runtime_element, web_driver)
        original_style = get_style(next_element_rt._runtime_element)
        highlight_element(next_element_rt._runtime_element)
        
        selected_element_screenshot = save_screenshot(
            web_driver,
            save_path=os.path.join(working_dir, "screenshots"),
            filename=visited_object.get_attribute('uuid') + ".png"
        )
        
        next_element._all_attributes['screenshot'] = selected_element_screenshot
        current_place.data = pdata
        
        if next_element_rt.is_attached():
            apply_style(next_element_rt._runtime_element, original_style)
        
        arc: Arc = trajectory.arcs[step]
        
        input_data = arc.data
        logger.debug(f"input data for this action={input_data}")
        if not next_element_rt.perform(web_driver, data=input_data):
            logger.debug(f"unable to perform action (selected: {next_element_rt})")
            return current_place
        else:
            logger.debug(f"perform action successful (selected:{next_element_rt})")
        
        
        next_place = [pl for pl in [arc.destination] if pl.name == trajectory.places[step+1].name][0]
        
        current_place =  next_place


def get_driver():
    options = Options()
    # options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(options=options)


def start(petriNets: dict, project_id=None):
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
        
        logger.debug(f"Start traverse for test case: {case_name}")
        
        visited_endnodes = []
        visited_places = []
        while True:
            while True:
                random_path, visited_places = select_path(petriNet, visited_places)
                if random_path.places[-1] in visited_endnodes:
                    continue
                else:
                    visited_endnodes.append(random_path.places[-1])
                    break

            logger.info(f"Length of random_path: {len(random_path)}")
        
            try:
                traverse(web_driver, objManager, random_path, working_dir, petriNet)
                if len(set(visited_places)) == len(petriNet.place()):
                    break
                
            except Exception as e:
                logger.exception(f'Unexpected error. {e}')
                web_driver.quit()
    
    web_driver.quit()
    # new_net.merge_places(object_manager=objManager)
    PetriNet.save(petriNet, f"{working_dir}/petri-net.pkl")
    logger.debug(f'CRAWLING_END: {timestamp()}')


if __name__ == "__main__":
    pnc.SCRIPT_INPUT_DIR = "test_generator/GroovyParser/Data"
    pnc.SCRIPT_OUTPUT_DIR = "test_generator/GroovyParser/Output"
    pnc.GROOVY_PARSER_DIR = "test_generator/GroovyParser"
    proj = "/Users/luong.nguyen/Katalon Studio/Test"
    
    # net, scripts = pnc.construct_code_based_petrinet(proj)
    testcases = pnc.fetch_script_paths(proj)
    
    nets = []
    script_lists = []

    for case, script_list in testcases.items():
        net, scripts = pnc.construct_code_based_petrinet_(proj, (case, script_list))
        
        nets.append(net)
        script_lists.append(script_list)

    new_nets = {}

    for case_name, net, scripts in zip(testcases.keys(), nets, script_lists):
        new_net = pnc.codeBased_to_actionBased(proj, net, scripts)
        new_nets[case_name] = new_net
    
    # url = "http://localhost:3000/addressbook/index.php"
    # url = "http://localhost/phpfusion_v8/news.php"
    # url = "http://localhost:3000/ppma_052/index.php?r=entry/index"
    # url = "http://localhost/phpfusion/files/home.php"

    start(new_nets)
