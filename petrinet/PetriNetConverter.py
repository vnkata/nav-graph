"""
This script is for generating action-based petrinet from Katalon test scripts by first parsing the scripts to code-based petrinet then convert that petrinet to action-based.
"""

import os
import subprocess
import shutil
import sys
import re
from typing import Dict, List, Tuple
from copy import deepcopy
from element.Element import ActionableElement, ElementFactory
from test_generator.StateGraph import snakes
from test_generator.StateGraph.TestStep import TestStep
sys.path.append("./test_generator/StateGraph/")
sys.path.append("./test_generator/StateGraph/snakes")
from . import PetriNet as actptn
from .Assertion import BaseAssertion
from test_generator.StateGraph.PetriNet import CustomPetriNet
import test_generator.StateGraph.snakes.nets as nets
from utils import randomid
from collections import deque
import xmltodict as x2d

from loguru import logger

SCRIPT_INPUT_DIR = "test_generator/GroovyParser/Data"
SCRIPT_OUTPUT_DIR = "test_generator/GroovyParser/Output"
GROOVY_PARSER_DIR = "test_generator/GroovyParser"
GROOVY_PARSER_PKG = "mypackage"

def create_default_place_data():
    return {
        'access_time': None,
        'current_title': None,
        'current_url': None,
        'screenshot': None,
        'num_objects': None,
        'visited_flags': [],    
        'obj_uuids': [],    
        'selected': [],
        'assertions': [],
        "from_test_script": True,
        "is_augmented": False
    }

def create_default_act_element_data():
    return {
        "accessible_name": None,
        "class": None,
        "href": None,
        "id": None,
        "innerHTML":  None,
        "innerText": None,
        "is_displayed": None,
        "is_enabled": None,
        "is_selected": None,
        "location": None,
        "outerHTML": None,
        "rect": None,
        "size": None,
        "style": None,
        "tag_name": None,
        "text": None,
        "title": None,
        "type": None,
        "uuid": None,
        "from_test_script": True,
        "is_augmented": False,
        "selectors": {
            "css": None,
            "xpath": {
                "any": set()
            }
        }
    }

def fetch_script_paths(proj_path: str):
    """
    Return a dictionary of all groovy test cases available in the path to Katalon test project. The dictionary maps from the test case names to their test script paths.

    Parameters
    ----------
    proj_path : str
        The path to a Katalon Studio test project directory
    """
    test_scripts = {}
    script_dir = os.path.join(proj_path, "Scripts")
    test_case_names = os.listdir(script_dir)
    for case in test_case_names:
        if not case.startswith('.') and os.path.isdir(os.path.join(script_dir, case)):
            test_scripts[case] = []
            case_path = os.path.join(script_dir, case)
            script_names = os.listdir(case_path)
            logger.info(f"Path of test case {case_path} & {script_names}")
            test_scripts[case].extend([os.path.splitext(name)[0] for name in script_names if name.endswith(".groovy")])

    return test_scripts

def prepare_test_script_input(proj_path: str):
    """
    Prepare the input test scripts by copying them from the project to the input directory of the generator module. Return the fetched test script name mapping.

    Parameters
    ----------
    proj_path : str
        Path to the Katalon Studio test project
    """
    scripts = fetch_script_paths(proj_path)
    logger.info(f"scripts dict: {scripts}")
    # Remove old inputs and outputs
    cwd = os.getcwd()
    os.chdir(SCRIPT_INPUT_DIR)
    [os.remove(f) for f in os.listdir() if os.path.isfile(f)]
    os.chdir(cwd)
    os.chdir(SCRIPT_OUTPUT_DIR)
    [os.remove(f) for f in os.listdir() if os.path.isfile(f)]
    os.chdir(cwd)
    # Copy test scripts from project path to input folder
    for case_name, script_list in scripts.items():
        for script in script_list:
            in_path = os.path.join(proj_path, "Scripts", case_name, script + ".groovy")
            shutil.copy(in_path, SCRIPT_INPUT_DIR)
    return scripts

def prepare_test_script_input_(proj_path: str, script: tuple):
    """
    Prepare the input test scripts by copying them from the project to the input directory of the generator module. Return the fetched test script name mapping.

    Parameters
    ----------
    proj_path : str
        Path to the Katalon Studio test project
    """
    # Remove old inputs and outputs
    cwd = os.getcwd()
    os.chdir(SCRIPT_INPUT_DIR)
    [os.remove(f) for f in os.listdir() if os.path.isfile(f)]
    os.chdir(cwd)
    os.chdir(SCRIPT_OUTPUT_DIR)
    [os.remove(f) for f in os.listdir() if os.path.isfile(f)]
    os.chdir(cwd)
    # Copy test scripts from project path to input folder
    script_dict = {script[0]: script[1]}
    for case_name, script_list in script_dict.items():
        for script in script_list:
            in_path = os.path.join(proj_path, "Scripts", case_name, script + ".groovy")
            shutil.copy(in_path, SCRIPT_INPUT_DIR)
    return script_dict

def call_groovy_parser(proj_path: str):
    """
    Call the groovy parser to parse the test scripts to a valid format in order to parse into a code-based petri-net. Return the fetched test script name mapping.

    Parameters
    ----------
    proj_path : str
        Path to the Katalon Studio test project
    """
    # Prepare the input scripts
    scripts = prepare_test_script_input(proj_path)
    # Call the groovy parser from shell command to parse the groovy files to txt files
    curdir = os.getcwd()
    try:
        if not os.path.exists(os.path.join(GROOVY_PARSER_DIR, GROOVY_PARSER_PKG)):
            subprocess.run(["make", "build"], cwd=GROOVY_PARSER_DIR, check=True, capture_output=True)
        subprocess.run(["make", "run"], cwd=GROOVY_PARSER_DIR, check=True, capture_output=True)
    except subprocess.CalledProcessError as procerr:
        logger.exception("Error: Make process failed. Unable to parse test scripts.")
        # raise Exception(procerr)
    os.chdir(curdir)
    logger.info("Successfully called the Groovy Parser on input test scripts!")
    return scripts

def call_groovy_parser_(proj_path: str, script):
    """
    Call the groovy parser to parse the test scripts to a valid format in order to parse into a code-based petri-net. Return the fetched test script name mapping.

    Parameters
    ----------
    proj_path : str
        Path to the Katalon Studio test project
    """
    # Prepare the input scripts
    scripts = prepare_test_script_input_(proj_path, script)
    # Call the groovy parser from shell command to parse the groovy files to txt files
    curdir = os.getcwd()
    try:
        if not os.path.exists(os.path.join(GROOVY_PARSER_DIR, GROOVY_PARSER_PKG)):
            subprocess.run(["make", "build"], cwd=GROOVY_PARSER_DIR, check=True, capture_output=True)
        subprocess.run(["make", "run"], cwd=GROOVY_PARSER_DIR, check=True, capture_output=True)
    except subprocess.CalledProcessError as procerr:
        logger.exception("Error: Make process failed. Unable to parse test scripts.")
        # raise Exception(procerr)
    os.chdir(curdir)
    logger.info(f"Successfully called the Groovy Parser on input test scripts: {script[0]}!")
    return scripts

def construct_code_based_petrinet_(proj_path: str, script, render_to_file=None):
    """
    Construct a code-based petri-net from Katalon Studio test scripts using the output of Groovy Parser. Return a tuple of the constructed petri-net and the fetched test script name mapping.  
    If render_to_file is a path to an image file, the constructed petrinet will be rendered as an image to that path. Otherwise, the renderer won't be called. 

    Parameters
    ----------
    proj_path : str
        Path to the Katalon Studio test project
    render_to_file: str
        Path to an output image file if the petrinet needs to be rendered.
    """
    def get_groovy_parser_outputs():
        outputs = []
        files = os.listdir(SCRIPT_OUTPUT_DIR)
        for f in files:
            fpath = os.path.join(SCRIPT_OUTPUT_DIR, f)
            fpath = fpath.replace("\\","/")
            outputs.append(fpath)
        return outputs
    
    script_dict = call_groovy_parser_(proj_path, script)
    input_list = get_groovy_parser_outputs()
    petrinet = CustomPetriNet()
    for i in input_list:
        petrinet.insert_a_testcase(i)
    if render_to_file is not None:
        petrinet.render(render_to_file)
    return petrinet, script_dict

def construct_code_based_petrinet(proj_path: str, render_to_file=None):
    """
    Construct a code-based petri-net from Katalon Studio test scripts using the output of Groovy Parser. Return a tuple of the constructed petri-net and the fetched test script name mapping.  
    If render_to_file is a path to an image file, the constructed petrinet will be rendered as an image to that path. Otherwise, the renderer won't be called. 

    Parameters
    ----------
    proj_path : str
        Path to the Katalon Studio test project
    render_to_file: str
        Path to an output image file if the petrinet needs to be rendered.
    """
    def get_groovy_parser_outputs():
        outputs = []
        files = os.listdir(SCRIPT_OUTPUT_DIR)
        for f in files:
            fpath = os.path.join(SCRIPT_OUTPUT_DIR, f)
            fpath = fpath.replace("\\","/")
            outputs.append(fpath)
        return outputs
    
    script_dict = call_groovy_parser(proj_path)
    input_list = get_groovy_parser_outputs()
    petrinet = CustomPetriNet()
    for i in input_list:
        petrinet.insert_a_testcase(i)
    if render_to_file is not None:
        petrinet.render(render_to_file)
    return petrinet, script_dict

def parse_obj_repo_path(proj_path: str, step_info: TestStep):
    # Parse the path to object repository
    try: 
        match = re.search(".*findTestObject\(\'(.+?)\'\)", step_info.input[0].code)
    except AttributeError:
        match = None
    obj_path: str
    if match:
        obj_path = match.group(1)
    else:
        raise Exception(f"Unsupported code in test script: {step_info.input[0].to_code()}")
    obj_name = os.path.basename(obj_path)
    test_name = os.path.basename(os.path.dirname(obj_path))
    obj_path = os.path.join(proj_path, "Object Repository", test_name, obj_name + ".rs")
    return obj_path, test_name, obj_name

def make_trans_from_step_info(path_info: Tuple[str, str, str], step_info: TestStep, obj_repo: Dict[str, ActionableElement]):
    elementFactory = ElementFactory()
    obj_path = path_info[0]
    obj_name = path_info[2]
    #repo_key = test_name + "/" + obj_name
    repo_key = obj_name
    # If the actionable element already exists
    if obj_repo.get(repo_key, None) is not None:
        # If the supported action is new, add new supported action
        # if obj_repo[repo_key]["transition"].get(step_info.action, None) is None:
        obj_repo[repo_key]["obj"]._supported_actions.append(step_info.action)
        # Create a new transition object for this actionable element
        obj_repo[repo_key]["transition"][step_info.action] = actptn.ActionableTransition(
            "T" + randomid(), 
            obj_repo[repo_key]["obj"], 
            step_info.action)
        return obj_repo[repo_key]["transition"][step_info.action]
    # Else parse the properties file in the project's object repository
    with open(obj_path) as file:
        obj = x2d.parse(file.read()) # return a dictionary
        obj = obj["WebElementEntity"]
    data_dict = create_default_act_element_data()
    # Parse the object name for necessary properties
    name: str = obj["name"]
    splitted_name = name.split("_")
    data_dict["tag_name"] = splitted_name[0]
    try:
        data_dict["accessible_name"] = splitted_name[1]
    except IndexError:
        data_dict["accessible_name"] = ""
    # Parse the properties list
    if obj.get("webElementProperties", None) is not None:
        for property in obj["webElementProperties"]:
            if property["name"] == "tag":
                data_dict["tag_name"] = property["value"]
            elif property["name"] == "xpath":
                data_dict["selectors"]["xpath"]["any"].add(property["value"])
            else:
                data_dict[property["name"]] = property["value"]
    # Parse the selectors
    if obj.get("webElementXpaths", None) is not None:
        if isinstance(obj["webElementXpaths"], list):
            for xpath in obj["webElementXpaths"]:
                xpath_type = xpath["name"].split(":")[1]
            
                if data_dict["selectors"]["xpath"].get(xpath_type, None) is None:
                    data_dict["selectors"]["xpath"][xpath_type] = set([xpath["value"]])
                else:
                    data_dict["selectors"]["xpath"][xpath_type].add(xpath["value"])
        else:
            xpath = obj["webElementXpaths"]
            xpath_type = xpath["name"].split(":")[1]
                
            if data_dict["selectors"]["xpath"].get(xpath_type, None) is None:
                data_dict["selectors"]["xpath"][xpath_type] = set([xpath["value"]])
            else:
                data_dict["selectors"]["xpath"][xpath_type].add(xpath["value"])
    for selector in obj["selectorCollection"]["entry"]:
        if selector.get("value", None) is None:
            continue
        if selector["key"] == "CSS":
            data_dict["selectors"]["css"] = selector["value"]
        elif selector["key"] == "XPATH":
            if obj.get("webElementXpaths", None) is not None:
                continue
            else:
                data_dict["selectors"]["xpath"]["any"].add(selector["value"])
        else:
            data_dict["selectors"][selector["key"].lower()] = selector["value"]
    # Cast all xpath sets back to lists in order to be json serializable
    for xpathType in data_dict["selectors"]["xpath"].keys():
        data_dict["selectors"]["xpath"][xpathType] = list(data_dict["selectors"]["xpath"][xpathType])
    # Add a new entry to the object repository
    act_ele = elementFactory.from_dict(data_dict)
    if step_info.action not in act_ele._supported_actions:
        act_ele._supported_actions.append(step_info.action)
    obj_repo[repo_key] = {"obj": act_ele, "transition": {}}
    obj_repo[repo_key]["transition"][step_info.action] = actptn.ActionableTransition(
        "T" + randomid(), 
        obj_repo[repo_key]["obj"], 
        step_info.action)
    return obj_repo[repo_key]["transition"][step_info.action]



def codeBased_to_actionBased(proj_path: str, codePtn: CustomPetriNet, script_dict: Dict):
    output = actptn.PetriNet()
    ptn: nets.PetriNet = codePtn.net
    obj_repo = {} # Keep info of recorded web element in Katalon Studio tests
    called_test_places = {} # Keep the name of the leaf place for each called test case, key is the test case name
    ignored_places = deque(["initial-place"])

    # Iterate through the transitions that have root
    while ignored_places:
        ignored_place = ptn.place(ignored_places.popleft())
        for trans_name in list(ignored_place.post.keys()):
            trans = ptn.transition(trans_name)
            step_info = trans.step_info
            # Handle when the transition fires to root
            # If the action is opening the browser, ignore the next place
            if step_info.action == "openBrowser":
                ignored_places.extend(trans.post.keys())
            # If the action is navigating to url, the next place is a root
            elif step_info.action == "navigateToUrl":
                place_name = list(trans.post.keys())[0]
                place_data = create_default_place_data()
                for c in ptn.place(place_name).constraint:
                    place_data["assertions"].append(BaseAssertion(c, proj_path))
                place_data["current_url"] = step_info.input[0].value
                new_name = "P" + randomid() # New name may not be necessary if renaming it affects performance too much
                ptn.rename_node(place_name, new_name)
                new_place = actptn.Place(new_name, place_data)
                output.add_root(new_place)
            # If the action is calling a test case, find the leaf place of that test flow to replace the next place of the action
            elif step_info.action == "callTestCase":
                # Parse the code-based petrinet of the called test case
                match = re.search(".*findTestCase\(\'(.+?)\'\)", step_info.input[0].code)
                test_name: str
                if match:
                    test_name = match.group(1)
                else:
                    raise Exception(f"Unsupported code in test script: {step_info.input[0].code}")
                subgraph = CustomPetriNet(test_name)
                for script_name in script_dict[test_name]:
                    test_path = os.path.join(SCRIPT_OUTPUT_DIR, script_name + ".txt")
                    subgraph.insert_a_testcase(test_path)
                # Find the name of leaf place
                if called_test_places.get(test_name, None) is None:
                    for p in subgraph.net.place():
                        if len(p.post) == 0:
                            last_trans = subgraph.net.transition(list(p.pre.keys())[0])
                            if last_trans.step_info.action == "closeBrowser":
                                called_test_places[test_name] = list(last_trans.pre.keys())[0]
                            else:
                                called_test_places[test_name] = p.name
                # Reconnect the leaf place of the called test to the transitions of the next place of the action
                next_place = ptn.place(list(trans.post.keys())[0])
                for next_trans in next_place.post.keys():
                    ptn.add_input(called_test_places[test_name], next_trans, nets.Variable('o'))
                ptn.remove_place(next_place.name) # Remove the next place from the petri-net
            # Remove the transition connected to the ignored place after handling it
            ptn.remove_transition(trans_name)
        # Remove the ignored place after done
        ptn.remove_place(ignored_place.name)
                        
    # Handle the remaining transition that doesn't fire to root
    for trans in ptn.transition():
        step_info = trans.step_info
        if step_info.action in ["If", "Else", "Try", "Catch", "For", "While"]:
            # TODO: Handle logical transitions
            continue
        act_ele = None
        new_trans: actptn.ActionableTransition       
        if len(step_info.input) > 0 and not step_info.action.startswith('switchTo'):
            path_info = parse_obj_repo_path(proj_path, step_info)
            # Create a new actionable transition if the actionable element is not in obj_repo
            # Or get the existing transition from obj_repo
            new_trans = make_trans_from_step_info(path_info, step_info, obj_repo)
        else:
            # If the transition is a non-element action
            new_trans = actptn.ActionableTransition("T" + randomid(), act_ele, step_info.action)
        output.add_node(new_trans)
        # A Transition in code-based petri-net is guaranteed to only have 1 input and 1 output place
        # Add/Connect previous place to the transition in the new petrinet
        in_place_name: str = list(trans.pre.keys())[0]
        if not in_place_name.startswith("P"):
            new_name = "P" + randomid()
            ptn.rename_node(in_place_name, new_name)
            in_place_name = new_name
        if output.place(in_place_name) is None:
            place_data = create_default_place_data()
            for c in ptn.place(in_place_name).constraint:
                place_data["assertions"].append(BaseAssertion(c, proj_path))
            new_place = actptn.Place(in_place_name, place_data)
            output.add_node(new_place)
        output.add_arc(output.place(in_place_name), output.transition(new_trans.name))
        # Skip the next place and the input value if the transition is closeBrowser
        if step_info.action == "closeBrowser":
            continue
        # Add/Connect next place to the transition in the new petrinet
        out_place_name: str = list(trans.post.keys())[0]
        if not out_place_name.startswith("P"):
            new_name = "P" + randomid()
            ptn.rename_node(out_place_name, new_name)
            out_place_name = new_name
        if output.place(out_place_name) is None:
            place_data = create_default_place_data()
            for c in ptn.place(out_place_name).constraint:
                place_data["assertions"].append(BaseAssertion(c, proj_path))
            new_place = actptn.Place(out_place_name, place_data)
            output.add_node(new_place)
        # Create transition value tuple if the action needs other inputs
        transition_input = None
        if len(step_info.input) > 1:
            # TODO: will update more case
            if step_info.action not in ['sendKeys']:
                transition_input = [i.value for i in step_info.input[1:]]
            else:
                transition_input = [i.code for i in step_info.input[1:]]
        elif step_info.action.startswith('switchTo'):
            transition_input = step_info.input[0].value
        output.add_arc(output.transition(new_trans.name), output.place(out_place_name), data=transition_input)
        # Add history to transition
        new_trans.add_history(in_place_name, out_place_name)
    return output