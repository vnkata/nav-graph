import os
from os.path import isfile, join
# import glob
import shutil
import sys
import inspect
import os.path
import datetime
# from StateGraph.ReportReader import ReportReader
# import subprocess

include_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
include_dir += '/StateGraph'
sys.path.insert(0, include_dir) 

# from StateGraph.StateParser import StateParser
from StateGraph.PetriNet import CustomPetriNet
# from StateGraph.TestCaseOptimizer import TestCaseOptimizer
# from TestCaseAdder import TestAdder
# from StateGraph.GeneratingStrategy import Strategy
# from StateGraph.SuiteSelection import SuiteSelection

import config
# from StateGraph.Graph import Graph

def get_all_files(dir_path):
    return [join(dir_path, f) for f in os.listdir(dir_path) if isfile(join(dir_path, f))]

def clean_workspace():
    files = get_all_files(config.OUTPUT_DIR)
    for f in files:
        os.remove(f)

def clean_dir(dir):
    for filename in os.listdir(dir):
        file_path = os.path.join(dir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def beautify_code():
    t = os.system('bash Beautifier/bin/format Output')
    print(t)

now = datetime.datetime.now()
code = now.strftime("%Y%m%d_%H%M%S")
clean_dir(config.LOG_DIR)

def write_log(msg):
    print(msg,flush=True)

def start_timer(msg = ""):
    global now
    now = datetime.datetime.now()
    write_log(msg + f" starts at {now}")
def end_timer(msg = ""):
    global now
    write_log(msg + f" ends at {datetime.datetime.now()}")
    write_log(msg + f" took {datetime.datetime.now()-now} to complete")

def main():
    sys.stdout = open(config.LOG_DIR + code + " run_log.txt", 'w')
    sys.stderr = open(config.LOG_DIR + code + " err_log.txt", 'w')

    global now
    clean_dir(config.FTEST_DIR + "Original/")
    names = get_all_files(config.TEST_DIR)
    g = CustomPetriNet()
    # g = Graph()
    for i in range(len(names)):
        #write_log(f'Processing {names[i]}')
        g.insert_a_testcase(names[i])
    #    g.summary()
    #g.render(f'Visualization/Moodle-14-Complete.png')
    
    # ======== TODO: Convert custom petri-net g to action-based petri-net
    print("Finished!")
    # ===================================================================
    
    # write_log("\nProcessed {0} tests".format(i+1))
    # clean_dir(config.OUTPUT_RAW_DIR)
    # start_timer("Initializing net")
    # conquerer = Strategy(g.net)
    # end_timer("Initializing net")
    # adder = TestAdder()
    # n = 50
    # coverage_on_exec = [] ; converge_rate = 20
    # for i in range(n):
    #     write_log(f'------------------------------------Iteration {i+1}------------------------------------')
    #     clean_workspace()

    #     start_timer("Generating")
    #     log = conquerer.generate_suite()
    #     write_log(log)
    #     log = conquerer.publish()
    #     write_log(log)
    #     end_timer("Generating")

    #     adder.self_check()
    #     if adder.sessionID == None:
    #         print("Session ID is None")
    #         break  
    #     adder.run()
        
    #     #run KRE with os.something
    #     start_timer("Test execution")
    #     f_list = set(glob.glob(config.KATALON_DIR + "Reports/*", recursive=False))
    #     project_path = "-projectPath=" + config.KATALON_DIR + config.K_PROJECT_NAME
    #     test_suite = "-testSuitePath=Test Suites/" + adder.sessionID
    #     fout = open(config.LOG_DIR + "KRE.txt", 'w')
    #     ferr = open(config.LOG_DIR + "KRE_errors.txt", "w") 
    #     subprocess.call([config.KRE_DIR + "katalonc.exe", """-noSplash""", """-runMode=console""", test_suite, project_path, """-retry=0""", """-retryStrategy=immediately""",
    #     """-browserType=Chrome""", config.API_KEY, """--config -webui.autoUpdateDrivers=true"""],stdout=fout,stderr=ferr)
    #     end_timer("Test execution")

    #     #read report & summarize
    #     newf_list = set(glob.glob(config.KATALON_DIR + "Reports/*", recursive=False))
    #     new_report = list(newf_list - f_list)
        
    #     pattern = new_report[0] + "/**/**/*.csv"
    #     write_log("Expect reports at: " + new_report[0] + "")
    #     rpreader = None
    #     for path in glob.glob(pattern, recursive=True):
    #         rpreader = ReportReader(path, adder.sessionID)
    #     passed, failed = rpreader.summarize()

    #     #pass in conquerer
    #     log, on_exec = conquerer.read_report(passed, failed)
    #     coverage_on_exec.append(on_exec)
    #     write_log(log)

    #     #clean up katalon project
    #     log = adder.cleanTrace()
    #     #write_log(log)

    #     conquerer.write_log_tests()
        
    #     if len(coverage_on_exec) >= converge_rate:
    #         tmp = coverage_on_exec[len(coverage_on_exec)-converge_rate:]
    #         if all(x==tmp[0] for x in tmp):
    #             print("Convergence on execution reached. Stop iterative generation")
    #             break

    ## ANY CODE BELOW THIS COMMENT IS DISCARDED
    
    # optimizer = TestCaseOptimizer(g)
    # optimizer.optimize()

    #     subgraph = StateParser.parse_a_testcase(name)
    #     subgraphs.append(subgraph)
        
    # reduced = frequentItemList(subgraphs)
    
    # for subgraph in reduced:
    #     g.merge(subgraph)

    # g.summary('Everleague.html')
    # g.save()
    # t = g.generate()
    # print(t)
    # beautify_code()

# def test():
#     names = get_all_files(config.TEST_DIR)
#     g = StateParser.parse_a_testcase(names[13])
#     g.summary()



if __name__ == '__main__':
    main()