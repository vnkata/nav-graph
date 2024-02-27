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

#suite = SuiteSelection(folder)
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

# for i in range(5):
#     start_timer("\nTabu search")
#     suite.tabu_search(eval_func = 'minimal',max_iter=100,drop_rate=13,top=7)
#     end_timer("Tabu search")

default_retry = 3
default_iter = 100
default_drop_rate = 13
default_top = 2
DATASET_LEN = 4
def restore_default():
    global default_retry, default_iter, default_drop_rate, default_top
    default_retry = 2
    default_iter = 100
    default_drop_rate = 25
    default_top = 1

def sort_func(key):
    return key[1]

def tune_retry(default_retry, default_iter, default_drop_rate, default_top, goal):
    #Retry tuning
    print("Retry tuning",flush=True)
    retry_arr = [2, 3, 5, 7, 9, 11, 13]
    res = []
    for param in retry_arr:
        reduction_sum = 0
        
        for dataset in [moodle_29,moodle_14,moodle_7,element_17]:
            #print("\n")
            suite = SuiteSelection(dataset)
            #for eval_fun in ['minimal','balance','duplicate']:
            reduction = 0
            for k in range(param):
                pack = suite.tabu_search(eval_func= goal, max_iter=default_iter,drop_rate=default_drop_rate,top=default_top)
                reduction = 1 - pack[2]/pack[3] if pack[2] < pack[3] else 0
                reduction_sum += reduction

        res.append([param, round(reduction_sum/(param*DATASET_LEN),4)])
    res.sort(key=sort_func,reverse=True)
    print("Results: ", res)
    return res[0][0] , default_iter, default_drop_rate, default_top

def tune_iteration(default_retry, default_iter, default_drop_rate, default_top, goal):
    #Iteration tuning
    print("Iteration tuning",flush=True)
    iter_arr = [50, 100, 150, 200, 250, 300]
    res = []
    for param in iter_arr:
        reduction_sum = 0
        
        for dataset in [moodle_29,moodle_14,moodle_7,element_17]:
            #print("\n")
            suite = SuiteSelection(dataset)
            #for eval_fun in ['minimal','balance','duplicate']:
            reduction = 0
            for k in range(default_retry):
                pack = suite.tabu_search(eval_func= goal, max_iter=param,drop_rate=default_drop_rate,top=default_top)
                reduction = 1 - pack[2]/pack[3] if pack[2] < pack[3] else 0
                reduction_sum += reduction

        #print(f"\nParam {param} - Reduction sum {round(reduction_sum,4)}\n")
        res.append([param, round(reduction_sum/(default_retry*DATASET_LEN),4)])
    res.sort(key=sort_func,reverse=True)
    print("Results: ", res)
    return default_retry, res[0][0], default_drop_rate, default_top

def tune_drate(default_retry, default_iter, default_drop_rate, default_top, goal):
    #drop rate tuning
    print("Drop rate tuning",flush=True)
    drate_arr = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    res = []
    for param in drate_arr:
        reduction_sum = 0
        
        for dataset in [moodle_29,moodle_14,moodle_7,element_17]:
            #print("\n")
            suite = SuiteSelection(dataset)
            #for eval_fun in ['minimal','balance','duplicate']:
            reduction = 0
            for k in range(default_retry):
                pack = suite.tabu_search(eval_func= goal, max_iter=default_iter,drop_rate=param,top=default_top)
                reduction = 1 - pack[2]/pack[3] if pack[2] < pack[3] else 0
                reduction_sum += reduction

        #print(f"\nParam {param} - Reduction sum {round(reduction_sum,4)}\n")
        res.append([param, round(reduction_sum/(default_retry*DATASET_LEN),4)])
    res.sort(key=sort_func,reverse=True)
    print("Results: ", res)
    return default_retry, default_iter , res[0][0], default_top

def tune_top(default_retry, default_iter, default_drop_rate, default_top, goal):
    #top neighbors tuning
    print("Search space tuning", flush=True)
    top_arr = [1, 2, 3, 5, 7, 11, 13]
    res = []
    for param in top_arr:
        reduction_sum = 0
        
        for dataset in [moodle_29,moodle_14,moodle_7,element_17]:
            #print("\n")
            suite = SuiteSelection(dataset)
            #for eval_fun in ['minimal','balance','duplicate']:
            reduction = 0
            for k in range(default_retry):
                pack = suite.tabu_search(eval_func= goal, max_iter=default_iter,drop_rate=default_drop_rate,top=param)
                reduction = 1 - pack[2]/pack[3] if pack[2] < pack[3] else 0
                reduction_sum += reduction

        #print(f"\nParam {param} - Reduction sum {round(reduction_sum,4)}\n")
        res.append([param, round(reduction_sum/(default_retry*DATASET_LEN),4)])
    res.sort(key=sort_func,reverse=True)
    print("Results: ", res)
    return default_retry, default_iter , default_drop_rate, res[0][0]

def tabu_with_settings(retry, iter, drate, top, goal):
    #Best settings here we go!
    start_timer("\nRunning using best parameters")
    print("No. retry:", retry)
    print("No. iteration:", iter)
    print("Search space factor:", top)
    print("Drop rate:", drate)
        
    for dataset in [moodle_29,moodle_14,moodle_7,element_17]:
        #print("\n")
        suite = SuiteSelection(dataset)
        #for eval_fun in ['minimal','balance','duplicate']:
        min_sol = []; min_val = float("inf") ; reduction_sum = 0
        for k in range(retry):
            pack = suite.tabu_search(eval_func= goal, max_iter=iter,drop_rate=drate,top=top)
            if pack[2] < min_val:
                min_val = pack[2] ; min_sol = pack

        cur_reduction = 1 - min_sol[2]/min_sol[3] if min_sol[2] < min_sol[3] else 0
        print(f"Best {round(min_sol[2],3)} - Original {min_sol[3]} - Reduction rate: {round(cur_reduction,3)}",flush=True)

    end_timer("Running using best parameters")

tune_call = { 1 : tune_drate, 2 : tune_top , 3 : tune_iteration, 4 : tune_retry}


goal_order = ['minimal', 'balance', 'duplicate']
# for i in range(3):
#     goal = goal_order[i]
#     print("Optimize goal: ", goal)
#     used_order = []
#     for j in range(5):
#         restore_default()
#         param = [default_retry, default_iter, default_drop_rate, default_top]
#         order = [1,2,3,4]
#         while order in used_order:
#             random.shuffle(order)
#         used_order.append(order)
#         print("Tune order", order)

#         start_timer("Tuning")
#         for k in order:
#             param = tune_call[k](param[0], param[1], param[2], param[3], goal)
#         end_timer("Tuning")

#         tabu_with_settings(param[0], param[1], param[2], param[3], goal)

param = [0,0,0,0]

res = [[150,150,300,100,100],
        [7,11,5,13,11],
        [7,7,7,5,13],
        [2,7,13,7,7] ]
print("Using voting approach for param")
for i in range(len(res)):
    tmp = sorted(dict(Counter(res[i])).items(), key=lambda x: x[1])
    param[i] = tmp[-1][0]
tabu_with_settings(param[3],param[0],param[2],param[1],'minimal')

print("Using mean approach for param")
for i in range(len(res)):
    param[i] = int(sum(res[i])/len(res[i]))
tabu_with_settings(param[3],param[0],param[2],param[1],'minimal')

res = [ [300,300,250,250,250] ,
        [11,7,13,13,13] ,
        [7,5,13,5,7] ,
        [11,7,7,11,3] ]
print("Using voting approach for param")
for i in range(len(res)):
    tmp = sorted(dict(Counter(res[i])).items(), key=lambda x: x[1])
    param[i] = tmp[-1][0]
tabu_with_settings(param[3],param[0],param[2],param[1],'balance')

print("Using mean approach for param")
for i in range(len(res)):
    param[i] = int(sum(res[i])/len(res[i]))
tabu_with_settings(param[3],param[0],param[2],param[1],'balance')

res = [ [250,200,150,200,150],
        [13,7,11,7,13],
        [5,7,5,7,11],
        [3,3,5,3,9] ]
print("Using voting approach for param")
for i in range(len(res)):
    tmp = sorted(dict(Counter(res[i])).items(), key=lambda x: x[1])
    param[i] = tmp[-1][0]
tabu_with_settings(param[3],param[0],param[2],param[1],'duplicate')

print("Using mean approach for param")
for i in range(len(res)):
    param[i] = int(sum(res[i])/len(res[i]))
tabu_with_settings(param[3],param[0],param[2],param[1],'duplicate')






notification.notify(title = """Debug.py finished""", message = "Successful")