import random
import sys
from tracemalloc import start
import config
from os.path import isfile, join
import os
import re
import copy
from StateGraph.SuiteSelection import SuiteSelection
import glob
import datetime
from plyer import notification
import numpy as np
from collections import Counter

sys.stdout = open(config.LOG_DIR + "run_log.txt", 'w') 
sys.stderr = open(config.LOG_DIR + "err_log.txt", 'w')

moodle_29 = config.ABS_DIR + "Moodle_29_act+asrt/" 
moodle_14 = config.ABS_DIR + "Moodle_14_act+asrt/"
moodle_7 = config.ABS_DIR + "Moodle_7_act+asrt/"
element_17 = config.ABS_DIR + "Element_17_act+asrt/"

now = datetime.datetime.now()
def start_timer(msg = ""):
    global now
    now = datetime.datetime.now()
    print(msg + f" starts at {now}",flush=True)
def end_timer(msg = ""):
    global now
    print(msg + f" ends at {datetime.datetime.now()}",flush=True)
    print(msg + f" took {datetime.datetime.now()-now} to complete\n",flush=True)

folder_dict = { 0: moodle_29, 1: moodle_14, 2: moodle_7, 3: element_17}
for i in folder_dict.values():
    suite = SuiteSelection(i)
    start_timer(i)
    suite.optimizer2(True)
    end_timer(i)
# suite.optimizer1()
# suite.opti1_pen_learn(alpha= 0.35)
# suite.optimizer3()
# suite.optimizer5()
# suite.optimizer4()

# start_timer("\nGreedy")
# suite.optimizer1()
# end_timer("Greedy")

# start_timer("\nGreedy with penalty")
# suite.opti1_pen_learn(alpha= 0.35)
# end_timer("Greedy with penalty")

# start_timer("\nGreedy")
# suite.optimizer1_1()
# end_timer("Greedy")