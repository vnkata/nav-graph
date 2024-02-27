#  Created by nphau on 11/20/22, 10:47 AM
#  Copyright (c) 2022 . All rights reserved.
#  Last modified 11/20/22, 10:47 AM
import json
from loguru import logger
import os
import datetime


def serialize(record):
    subset = {"timestamp": record["time"].timestamp(), "message": record["message"]}
    return json.dumps(subset)


def patching(record):
    record["extra"]["serialized"] = serialize(record)


def formatter(record):
    # Note this function returns the string to be formatted, not the actual message to be logged
    record["extra"]["serialized"] = serialize(record)
    return "{extra[serialized]}\n"


logger = logger.patch(patching)


def get_log_folder_name():
    return datetime.datetime.now().strftime('run-%d.%m.%Y-%H.%M.%S')


def get_working_dir(project_id):
    return f"db/running_logs/{project_id}/{get_log_folder_name()}"


def get_log_folder(project_id):
    return f"db/running_logs/{project_id}"


def get_log_file_path(project_id):
    return f"{get_log_folder(project_id)}/{project_id}.log"


def init_logger(project_id):
    file = get_log_file_path(project_id)
    if os.path.exists(file):
        os.remove(file)
    logger.remove(0)
    logger.add(file, format=formatter)
