#  Created by nphau on 11/13/22, 3:59 PM
#  Copyright (c) 2022 . All rights reserved.
#  Last modified 11/13/22, 3:59 PM
import os
import sys
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)
from datetime import datetime


def to_date(timestamp):
    if timestamp:
        return datetime.fromtimestamp(timestamp)
    else:
        return ""


def extract_value(item, key):
    try:
        return item[key]
    except:
        return ""


def duration(item):
    try:
        seconds = (item['endTime'] - item['startTime'])
        # seconds, milliseconds = divmod(milliseconds, 1000)
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        # seconds = seconds + milliseconds / 1000
        return f"{days} days, {hours} hours"
    except:
        return ""
