#  Created by nphau on 9/15/22, 11:56 PM
#  Copyright (c) 2022 . All rights reserved.
#  Last modified 9/15/22, 11:56 PM

import glob
import shutil

import numpy as np
import os
import json
import sys
from loguru import logger
import algorithm

sys.path.append('../../petrinet/')

shared_obj_repo = f"../running_logs/SHARED_OBJ_REPO/"
if not os.path.exists(shared_obj_repo):
    os.makedirs(shared_obj_repo)
    os.makedirs(shared_obj_repo + "all")
    os.makedirs(shared_obj_repo + "visited")
    for path in glob.glob(os.path.join("../running_logs/run-*/objects/all/", '*.*')):
        filename = os.path.basename(path)
        shutil.copy(path, shared_obj_repo + f"all/{filename}")
    for path in glob.glob(os.path.join("../running_logs/run-*/objects/visited/", '*.*')):
        filename = os.path.basename(path)
        shutil.copy(path, shared_obj_repo + f"visited/{filename}")
    for path in glob.glob(os.path.join("../running_logs/run-*/objects/all/", '*.*')):
        filename = os.path.basename(path)
        if not os.path.exists(shared_obj_repo + f"visited/{filename}"):
            shutil.copy(path, shared_obj_repo + f"visited/{filename}")


def get_petri_net_files(graph_id=None):
    if graph_id is not None:
        db_path = f"./db/running_logs/{graph_id}"
        if os.path.exists(db_path):
            return glob.glob(f"{db_path}/*/petri-net.pkl")
    return glob.glob("../running_logs/*/petri-net.pkl")


def get_obj_by_uuid(uuid):
    return f"../running_logs/SHARED_OBJ_REPO/visited/obj.{uuid}.json"


# a dirty hack to improve the load speed
# TODO: need to fix later
uuid_m = {}


def get_all_objs(selected_node):
    uuids = []
    uuid = selected_node.get("uuid", None)
    if uuid is not None:
        uuids.append(uuid)
    else:
        uuids = np.array(list(selected_node.get("object_uuids", {}).keys()))
    uuids = np.unique(uuids)
    files = {}
    for uuid in uuids:
        if uuid in uuid_m:
            files[uuid] = uuid_m[uuid]
        else:
            try:
                with open(get_obj_by_uuid(uuid), "r") as file:
                    data = json.load(file)
                    files[uuid] = data
                uuid_m[uuid] = data
            except Exception as e:
                logger.error(e)
    return files


def get_json_by_uuid(files, uuid):
    return json.loads(files).get(uuid)


def get_coordinates(element_object):
    uuid = element_object.get("uuid")
    rect = element_object.get("rect")
    x0 = rect.get("x")
    x1 = x0 + rect.get("width")
    y0 = rect.get("y")
    y1 = y0 + rect.get("height")
    return uuid, x0, x1, y0, y1


def find_objects_by_rect(selected_node, cmp_rect):
    uuid_files = get_all_objs(selected_node)
    cmp_x0 = cmp_rect.x0
    cmp_x1 = cmp_rect.x1
    cmp_y0 = cmp_rect.y0
    cmp_y1 = cmp_rect.y1
    result = []
    for element_object in uuid_files.values():
        uuid, x0, x1, y0, y1 = get_coordinates(element_object)
        if algorithm.compare_rects(x0, x1, y0, y1, cmp_x0, cmp_x1, cmp_y0, cmp_y1):
            print(f"{uuid} | {x0} - {x1} - {y0} - {y1}")
            result.append({
                "uuid": uuid,
                "object": element_object
            })
    return result


def find_objects_by_position(selected_node, cmp_x, cmp_y, cmp_z):
    uuid_files = get_all_objs(selected_node)
    result = []
    for element_object in uuid_files.values():
        uuid, x0, x1, y0, y1 = get_coordinates(element_object)
        if algorithm.is_point_inside_rect(cmp_x, cmp_y, x0, x1, y0, y1):
            print(f"{uuid} | {x0} - {x1} - {y0} - {y1}")
            result.append({
                "uuid": uuid,
                "object": element_object
            })
    return result
