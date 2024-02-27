import asyncio
from pathlib import Path
from re import A
from typing import Union
import chromedriver_binary
import random

from selenium import webdriver
from petrinet.PetriNet import Transition, Place, PetriNet
from element.operators import find_element
from petrinet.traversal_utils import select_random_path, create_trajectory
from repository.core import ObjectManager
from element.Element import RuntimeActionableElement, ActionableElement
import json
from loguru import logger
from utils import randomword
import random
import sys
import os
import json
from quart import websocket, Quart
from petrinet.AssertionU import dict2assertion, Assertion
sys.setrecursionlimit(1_000_000)

app = Quart(__name__)
SOCKET_PATH_SERVER = "/server"

# rm_special_charac = lambda x: x[0] + x[2:]

def check_assertion(assertion_file, objManager, driver):
    with open(assertion_file, "r") as fp:
        assertions = json.load(fp)
    
    for assertion in assertions:
        # logger.debug(f"assertion={assertion}")
        assertion_obj: Assertion = dict2assertion(assertion)
        # logger.debug(f"assertion_obj={assertion_obj}")
        if assertion_obj.verify(driver, objManager) == False:
            logger.debug(f"assertion_obj={assertion_obj} return : False")
            return False
        else:
            logger.debug(f"assertion_obj={assertion_obj} return : True")
    return True 

async def playback(driver, petriNet: PetriNet, objManager: ObjectManager, trajectory, websocket, logdir):

    logger.info (f"trajectory: {trajectory}")
    # current_place = trajectory.places[0] #petriNet.root[0]
    # driver.get(current_place.data.url)
    current_place: Place = None
    for r in petriNet.root:
        if r.name == trajectory.places[0].name:
            current_place = r
            break
    # driver.get(current_place.data.url.replace("phpfusion_v90310", "phpfusion_v90370"))
    driver.get("http://phpfusion_v90310.loc/home.php")

    if len(trajectory.transitions) == 0:
        logger.debug (f"no transition in the trajectory!, return root place~({str(petriNet.root)})")
        return petriNet.root[0]
    
    for step in range(len(trajectory.places)):
        logger.info(f"Access: current_place=[{current_place.name}], stored_place={trajectory.places[step]}, depth=[{step}]")
        await websocket.send_json(json.dumps({'type': 'UPDATE_CURRENT_POSITION', 'node': current_place.name, 'status': True})) 
        await asyncio.sleep(0.3)

        #
        if step >= len(trajectory.transitions):
            logger.info(f"finish navigating the the trajectory: {trajectory}")
            return current_place

        candidate_transitions = []
        for x in current_place.output_arc():
            if x.destination.name == trajectory.transitions[step].name:
                candidate_transitions.append(x.destination)
    
        next_transition: Transition = candidate_transitions[0]
        next_element: ActionableElement = objManager.get_object(next_transition.data.get_attribute('uuid'))
        if len(next_transition.output_arc()) == 0:
            logger.debug(f"transition~({next_transition}) does not contain any output_arc()")
            await websocket.send_json(json.dumps({'type': 'UPDATE_CURRENT_POSITION', 'node': next_transition.name, 'status': True}))
            await asyncio.sleep(0.3)
            return current_place

        next_element_rt: RuntimeActionableElement = find_element(next_element, driver) 
        if next_element_rt is None:
            logger.debug(f"element~({next_element.get_attribute('uuid')}) can not found!")
            await websocket.send_json(json.dumps({'type': 'UPDATE_CURRENT_POSITION', 'node': next_transition.name, 'status': False})) 
            await asyncio.sleep(0.3)
            return current_place

        next_element_rt.update_action(next_transition.transition_type)
        data = list(next_transition.output_arc())[0].data
        logger.debug(f"data={data}")
        if not next_element_rt.perform(driver, data=data):
            logger.debug(f"unable to perform action (selected: {next_element_rt})")
            await websocket.send_json(json.dumps({'type': 'UPDATE_CURRENT_POSITION', 'node': next_transition.name, 'status': False}))
            await asyncio.sleep(0.3)
            return current_place
        else:
            logger.debug(f"perform action successful (selected:{next_element_rt})")
            await websocket.send_json(json.dumps({'type': 'UPDATE_CURRENT_POSITION', 'node': next_transition.name, 'status': True})), 
            await asyncio.sleep(0.3)

        next_place = [pl.destination for pl in next_transition.output_arc() if pl.destination.name == trajectory.places[step+1].name][0]
        
        # assertion verification.
        assertion_file = os.path.join(os.path.split(os.path.abspath(logdir))[0], "ASSERTIONS", next_place.name, next_place.name + ".json")
        if os.path.exists(assertion_file):
            logger.info("Found an assertion file associated with this page ~> verify this place by checking custom assertions.")
            if not check_assertion(assertion_file, objManager, driver):
                logger.info("Check assertion failed !")
                await websocket.send_json(json.dumps({'type': 'UPDATE_CURRENT_POSITION', 'node': next_place.name, 'status': False}))
                await asyncio.sleep(0.3)
                return current_place                
        else:
            logger.info(f"{assertion_file} not found ~ no assertions for : {next_place.name} !")
        current_place =  next_place



async def run_all_paths():
    working_dir = "running_logs/run-10.08.2022-23.21.27"
    Path(os.path.join(".temp")).mkdir(parents=True, exist_ok=True)
    logger.add(f"{working_dir}/playback.log", backtrace=True, diagnose=True, level=20)

    petriNet = PetriNet.load(os.path.join("running_logs", 'merged_net.pkl'))
    objManager = ObjectManager(working_dir=working_dir)
    driver = webdriver.Chrome()

    visited_endnodes = []
    while True:
        # TODO: Re-factor this code later.
        while True:
            random_path = select_random_path(petriNet)
            if random_path.places[-1] in visited_endnodes:
                continue
            else:
                visited_endnodes.append(random_path.places[-1] )
                break

        logger.info("random_path: " + str(random_path))
        # await asyncio.gather(websocket.send_json(json.dumps({'type': 'INIT', 'value': list(map(lambda x: x.name, random_path['transitions'] + random_path['places']))})), asyncio.sleep(3))
        await websocket.send_json(json.dumps({'type': 'INIT', 'value': list(random_path.transitions + random_path.places)}))
        await asyncio.sleep(3)
        #await asyncio.gather(playback(driver, petriNet, objManager, random_path, websocket, working_dir))
        await playback(driver, petriNet, objManager, random_path, websocket, working_dir)


async def go_to_place(place_name:str):
    working_dir = "running_logs/run-10.08.2022-23.21.27"
    Path(os.path.join(".temp")).mkdir(parents=True, exist_ok=True)
    logger.add(f"{working_dir}/playback.log", backtrace=True, diagnose=True, level=20)

    petriNet = PetriNet.load(os.path.join("running_logs", 'merged_net.pkl'))
    objManager = ObjectManager(working_dir=working_dir)
    driver = webdriver.Chrome()

    # place_name = 
    target_place = petriNet.place(place_name)
    logger.info(f"Target place: {target_place}")
    trajectory = create_trajectory(target_place)

    a = websocket.send_json(json.dumps({'type': 'INIT', 'value': list(map(lambda x: x.name, trajectory.transitions + trajectory.places))}))
    b = asyncio.sleep(3)
    await asyncio.gather(a, b)
    await asyncio.gather(playback(driver, petriNet, objManager, trajectory, websocket, working_dir))
    logger.info("Done !!!")
    return

@app.websocket(f"{SOCKET_PATH_SERVER}")
async def ws():
    logger.info("Connecting to SERVER_SOCKET...")
    await websocket.accept()
    logger.info("Connected !")
    while True:
        logger.info ('Waiting for receiving new message..')
        message = await websocket.receive()
        message = json.loads(message)
        print ("message: ", message)
        message_t = message.get("type", 'Unknow') 
        if message_t == 'PLAY_TO_HERE':
            await go_to_place(place_name=message['value'])
            logger.debug("Task: PLAY_TO_HERE is finished")
        elif message_t == 'RUN_ALL':
            await run_all_paths()
            logger.debug("Task: RUN_ALL is finished")
        else:
            logger.info("This message's type has not implemented yet")


if __name__ == "__main__":
    app.run(port=5000)