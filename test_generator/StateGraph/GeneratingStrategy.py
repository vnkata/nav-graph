import datetime
import re
from StateGraph.PetriNet import CustomPetriNet
from StateGraph.CodeConverter import ImportIndex
import os
from os.path import isfile, join
import config
import copy
import random

def get_all_files(dir_path):
    return [join(dir_path, f) for f in os.listdir(dir_path) if isfile(join(dir_path, f))]

class Strategy:
    def __init__(self, net) -> None:
        im = ImportIndex()
        self.ims = im.data
        if len(self.ims) == 0:
            paths = get_all_files(config.ABS_DIR+"GroovyParser/Data/")
            if paths == []:
                print("GeneratingStrategy: No data to process")
                return
            for p in paths:
                im.read_import(p)
            self.ims = list(im.data)

        self.net = net
        self.start_place  = net._place['initial-place'] # initial place of all
        self.HDict = {} #store node.name : height
        self.HList = [] #store node.name in each height
        self.explore_net()

        self.exisiting_tests = []
        self.get_exisiting_test()
        
        self.raw_test_collections = [] #test step is trans name
        self.test_collections = [] #list of str, each ele is a test case, includes action test step

        self.delay_dict = {}
        self.record_delay()

        self.failed_tests = [] #each ele is a test stops at failed step
        self.passed_tests = [] #each ele is a passed test cases
        self.skip_nodes = set()
        self.read_log_tests()

        self.iter = -1
    
    def dfs_explore(self,node, height):
        trans = False
        if len(node.name.split(";;;")) == 3: #is trans
            trans = True
        self.stack.append(node.name)

        if not node.post.keys(): #close browser
            self.cntpath += 1

        if node.name not in self.recorder:
            self.recorder.append(node.name)

        if node.name not in self.HDict.keys(): #not exist yet
            self.HDict.update({node.name:height})
            while len(self.HList) < height + 1:
                self.HList.append([])
            self.HList[height].append(node.name)
        else: #node is already exist
            if self.HDict[node.name] > height: #the node can be reached in this path is shorter
                h = self.HDict[node.name]
                self.HList[h] = list(filter(lambda x: x != node.name, self.HList[h]))
                self.HList[height].append(node.name)
                self.HDict[node.name] = height

        for name in node.post.keys():
            if trans: #if this node is trans -> next node is place
                next_node = self.net._place[name]
            else:
                next_node = self.net._trans[name]
            if next_node.name not in self.stack:
                self.dfs_explore(next_node, height + 1)

        #if trans:
        self.stack.pop()
    
    def explore_net(self):
        self.cntplace = {}
        self.cntpath = 0
        self.recorder = []
        self.stack = []
        self.end_place = None
        node = self.start_place
        self.dfs_explore(node, 0)
        print("Total nodes(places & trans):", len(self.recorder))
        print("Total possible paths:", self.cntpath)

    def record_delay(self):
        self.delay_dict = {}
        paths = get_all_files(config.INPUT_DIR)
        for path in paths:
            with open(path,"r",encoding="utf8") as f:
                data = f.read()
            lines = list(filter(lambda x: x != "", data.split("\n")))
            for i in range(len(lines)-1,-1,-1):
                if lines[i][:11] == "WebUI.delay" and lines[i-1] not in self.delay_dict.keys(): #spot delay step and action step not in dict
                    self.delay_dict.update({re.sub(" ","",lines[i-1]):lines[i-1]+ "\n" +lines[i]}) #action step: action step + delay step
        print("Delay test steps found:", len(self.delay_dict.keys()))

    def get_exisiting_test(self):
        names = get_all_files(config.FTEST_DIR + "Original/")
        self.exisiting_tests = []
        for name in names:
            with open(name, "r", encoding="utf8") as f:
                raw = f.read().split("\n")
                self.exisiting_tests.append(raw) 
    
    def compare_tstep(self, ts1, ts2):
        return re.sub(" ","",ts1) == re.sub(" ","",ts2)

    def compare_tcase(self, tc1, tc2):
        if len(tc1) != len(tc2):
            return False
        for i in range(len(tc1)):
            if not self.compare_tstep(tc1[i],tc2[i]):
                return False

        return True

    def is_valid_path(self, tc):
        for f in self.failed_tests: #each ele (test case) has list of trans name
            if self.compare_tcase(tc,f):
                return False
        return True

    def raw_to_steps(self, test):
        ret= []
        for i in range(len(test)):
            steps = test[i].split(";;;")
            if i != 0:
                # assertions = []
                # if ";" in steps[0]: #has 2 or more assertions
                #     assertions += steps[0].split(';')
                # else:
                #     prev_trans = test[i-1].split(";;;")[1]
                #     asrt = re.sub("_p[0-9]+","",steps[0])
                #     if prev_trans != asrt:
                #         assertions += [steps[0]]
                place = steps[0]
                assertions = place.split(";:;")[1].split(";")
                assertions = list(map(lambda x: re.sub("_p[0-9]+","",x),assertions))
                ret += assertions
            ret += [steps[1]]
        ret = list(filter(lambda x: x!= '',ret))
        return ret

    def to_test_collections(self):
        for raw in self.raw_test_collections:
            test = self.raw_to_steps(raw)
            self.test_collections.append(test)

    def correct_test_steps(self):
        for j in range(len(self.test_collections)):
            teststeps = self.test_collections[j]
            for i in range(len(teststeps)):
                idx = teststeps[i].find('this.')
                if idx!= -1:
                    teststeps[i] = teststeps[i][:idx] + teststeps[i][idx+5:] #remove "this." from any test steps

                if re.sub(" ","",teststeps[i]) in self.delay_dict.keys():
                    teststeps[i] = self.delay_dict[re.sub(" ","",teststeps[i])]

            self.test_collections[j] = teststeps

    def publish(self):
        def get_cnt(cnt, maxc):
            ret = str(cnt)
            while len(ret) < len(str(maxc)):
                ret = "0" + ret
            return ret

        self.to_test_collections()
        self.correct_test_steps()
        cnt = 0
        write = ""
        self.iter += 1
        if not os.path.exists(config.OUTPUT_RAW_DIR + "Iter" + str(self.iter) + "/"):
            os.mkdir(config.OUTPUT_RAW_DIR + "Iter" + str(self.iter) + "/")
        for i in range(len(self.test_collections)):
            for j in range(len(self.exisiting_tests)):
                if self.compare_tcase(self.test_collections[i], self.exisiting_tests[j]):
                    write += f"Duplicate generated {i} - original {j}\n" 
            
            test_content = "\n".join(self.ims) + "\n\n\n" + "\n".join(self.test_collections[i])
            with open(config.OUTPUT_DIR + get_cnt(cnt,len(self.test_collections))+".groovy","w", encoding="utf8") as f:
                f.write(test_content)

            with open(config.OUTPUT_RAW_DIR + "Iter" + str(self.iter) + "/" + get_cnt(cnt,len(self.test_collections))+".groovy","w",encoding="utf8") as f:
                f.write(test_content)
            
            cnt += 1

        return write
        
    def write_log_tests(self):
        def get_cnt(cur,maxc):
            res = str(cur)
            while len(res) < len(str(maxc)): #padding for better look
                res = "0" + res
            return res

        folder = config.FTEST_DIR + "Fail/"
        files = get_all_files(folder)
        for f in files:
            os.remove(f)
        for i in range(len(self.failed_tests)):
            with open(folder + get_cnt(i,len(self.failed_tests)) + ".txt","w",encoding="utf8") as f:
                data = "\n".join(self.failed_tests[i])
                f.write(data)

        folder = config.FTEST_DIR + "Pass/"
        files = get_all_files(folder)
        for f in files:
            os.remove(f)
        for i in range(len(self.passed_tests)):
            with open(folder + get_cnt(i,len(self.passed_tests)) + ".txt","w",encoding="utf8") as f:
                data = "\n".join(self.passed_tests[i])
                f.write(data)

    def read_log_tests(self):
        names = get_all_files(config.FTEST_DIR +"Fail/")
        for name in names:
            with open(name,"r",encoding="utf8") as f:
                raw = f.read().split("\n")
                self.failed_tests.append(raw)

        names = get_all_files(config.FTEST_DIR +"Pass/")
        for name in names:
            with open(name,"r",encoding="utf8") as f:
                raw = f.read().split("\n")
                self.passed_tests.append(raw)

        for i in range(len(self.failed_tests)-1,-1,-1): #filter duplicates
            for j in range(i-1,-1,-1):
                if self.failed_tests[i] == self.failed_tests[j]:
                    self.failed_tests.pop(j) ; break

        for i in range(len(self.passed_tests)-1,-1,-1): #filter duplicates
            for j in range(i-1,-1,-1):
                if self.passed_tests[i] == self.passed_tests[j]:
                    self.passed_tests.pop(j) ; break

        with open(config.FTEST_DIR + "skipped.txt","r",encoding="utf8") as f:
            raw = f.read().split("\n")
        raw = list(filter(lambda x: x!="",raw))
        self.skip_nodes = set(raw)

    # def cal_resemblance(self):
    #     if self.visited == []:
    #         return 0
    #     dup = 0
    #     for s in self.stack:
    #         if s in self.visited:
    #             dup += 1
    #     return dup / len(self.stack)

    # def dfs_journal(self, node): #modified: a test should only have K% visited place
    #     self.stack.append(node.name)
    #     if node.name in self.dict.keys():
    #         self.dict[node.name] = self.dict[node.name] + 1
    #     else:
    #         self.dict.update({node.name:1})

    #     trans = False
    #     if len(node.name.split(";;;")) == 3:
    #         trans = True
    #     if trans:
    #         self.steps.append(node.name.split(";;;")[1]+"\n")

    #     get_names = list(node.post.keys())
    #     random.shuffle(get_names)
    #     for name in get_names:
    #         if trans: #if this node is trans -> next node is place
    #             next_node = self.net._place[name]
    #         else:
    #             next_node = self.net._trans[name]

    #         if not next_node.post.keys():#dict empty -> end of test
    #             self.cnt += 1
                
    #             if self.cal_resemblance() <= self.resemblance: # <= 70% resemblance
    #                 self.generated_cnt += 1
    #                 for s in self.stack:
    #                     if s not in self.visited:
    #                         self.visited.append(s)

    #                 #add test to collection
    #                 self.test_collections.append(copy.deepcopy(self.steps))

    #         #if next_node.name not in self.stack:# and next_node.name not in self.visited: #prevent self-loop -> conquer all paths
    #             #self.visited.append(node.name)
    #         if next_node.name in self.dict.keys() and self.dict[next_node.name] == 1: #maximum self-loop node is k
    #             continue
    #         self.dfs_journal(next_node)
            
    #     self.stack.pop()
    #     if self.dict[node.name] == 1:
    #         self.dict.pop(node.name)
    #     else:
    #         self.dict[node.name] = self.dict[node.name] - 1
    #     if trans:
    #         self.steps.pop()

    # def dfs(self):
    #     self.cnt = 0
    #     self.generated_cnt = 0
    #     self.recorder.clear()   
    #     self.test_collections.clear()
    #     self.visited = [] #visited places
    #     self.stack = [] #for backtracking
    #     self.steps = [] #for collecting test steps
    #     self.dict = {}
    #     self.resemblance = 0.9

    #     node = self.start_place
    #     self.dfs_journal(node)            
    #     print("------------------------------Summary------------------------------")
    #     print("Total generated tests:", self.generated_cnt)
    #     print("Total possible generated tests:", self.cnt)
    #     print("Resemblance test rate:", self.resemblance)
    #     print("Node coverage(place & trans): {0}/{1} = {2}".format(len(self.visited),len(self.recorder),len(self.visited)/len(self.recorder)))
    #     log_file = []
    #     with open(config.ABS_DIR + "StateGraph/Log/missed nodes.txt", "w") as f:
    #         for p in self.recorder:
    #             if p not in self.visited:
    #                 log_file.append(p)
    #         f.write("\n".join(log_file))

    # def dfsSA(self, node, A , must_cross):
    #     self.SAstack.append(node.name)
    #     trans = False
    #     if len(node.name.split(";;;")) == 3:
    #         self.SAsteps.append(node.name)
    #         trans = True

    #     if node.name == A: #destination reached or reach the end
    #         #must cross these nodes and not in failure
    #         if set(self.SAsteps) >= set(must_cross) and self.is_valid_path(self.SAsteps):
    #             self.SAminsteps = copy.deepcopy(self.SAsteps)
    #             self.SAminstack = copy.deepcopy(self.SAstack)
    #         self.SAstack.pop()
    #         if trans:
    #             self.SAsteps.pop()
    #         return

    #     get_names = list(node.post.keys())
    #     random.shuffle(get_names)
    #     for name in get_names:
    #         if trans: #if this node is trans -> next node is place
    #             next_node = self.net._place[name]
    #         else:
    #             next_node = self.net._trans[name]
                
    #         if not next_node.post.keys(): #dead-end
    #             continue

    #         if self.SAminstack != [] and len(self.SAstack) >= len(self.SAminstack): #already longer than prev found
    #             continue

    #         if next_node.name not in self.SAstack: # if next is trans and already visited then skip
    #             self.dfsSA(next_node,A, must_cross)

    #     self.SAstack.pop()
    #     if trans:
    #         self.SAsteps.pop()
        
            
    # def start_to_A(self, A, must_cross = []):
    #     self.SAsteps = [] #test steps to be considered
    #     self.SAminsteps = [] #shortest SA test steps
    #     self.SAstack = [] #node name to be considered
    #     self.SAminstack = [] #shortest SA nodes
    #     self.dfsSA(self.start_place,A, must_cross)

    # def AEcalScore(self, node, count, maxc): #dfs traversal to calculate 
    #     self.AEtmpstack.append(node.name)
    #     trans = False
    #     if len(node.name.split(";;;")) == 3:
    #         self.AEtmpsteps.append(node.name)
    #         trans = True

    #     get_names = list(node.post.keys())
    #     random.shuffle(get_names)
    #     mscore = 0
    #     for name in get_names:
    #         if trans: #if this node is trans -> next node is place
    #             next_node = self.net._place[name]
    #         else:
    #             next_node = self.net._trans[name]

    #         if not next_node.post.keys() or count + 1 == maxc: #reach end node or max count
    #             if next_node.name in self.visited or next_node.name in self.AEstack:
    #                 return 0
    #             else:
    #                 return 1 # cover one more node

    #         if (not trans and next_node.name not in self.AEtmpsteps and next_node.name not in self.AEsteps) or trans: # if next is trans and already visited then skip
    #             score = self.AEcalScore(next_node, count + 1, maxc)
    #             if mscore < score: mscore = score

    #     self.AEtmpstack.pop()
    #     if trans:
    #         self.AEtmpsteps.pop()

    #     if node.name in self.visited or node.name in self.AEstack:
    #         return mscore
    #     else:
    #         return mscore + 1
    
    # def A_to_end(self, A, X): #X is no. steps to cal ahead
    #     # X is no of steps to calculate ahead
    #     self.AEsteps = self.SAminsteps #store all test steps
    #     self.AEstack = self.SAminstack #store all node name
    #     if len(A.split(";;;")) == 3:
    #         node = self.net._trans[A]
    #     else:
    #         node = self.net._place[A]

    #     must_cross = [A]
    #     while node.post.keys():
    #         candidate = None
    #         mscore = -1
    #         trans = False
    #         if len(node.name.split(";;;")) == 3: #current is trans -> next is place
    #             trans = True

    #         for name in node.post.keys():
    #             self.AEtmpstack = []
    #             self.AEtmpsteps = []
    #             if trans: # next is place if now is trans
    #                 tmpnode = self.net._place[name]
    #             else:
    #                 tmpnode = self.net._trans[name]

    #             if not trans and tmpnode.name in self.AEsteps: # if next is trans and already visited then skip
    #                 continue
    #             score = self.AEcalScore(tmpnode, 1, X)
    #             if score > mscore:
    #                 mscore = score
    #                 candidate = tmpnode

    #         if candidate == None: #no path is beneficial -> choose last option
    #             candidate = tmpnode
                
    #         node = candidate
    #         self.AEstack.append(node.name)
    #         if not trans:
    #             self.AEsteps.append(node.name)

    #         if not self.is_valid_path(self.AEsteps): #find the shortest path go through A to the current conquered node
    #             self.start_to_A(node.name,must_cross) #stack reset in func
    #             if self.SAminsteps == [] and self.SAminstack == []:
    #                 #fix no valid SA -> randomly pick a path that cross A
    #                 print("Stuck at", A)
    #                 print("No valid path - Trying alternative solution")
    #                 print(f"Test suite has {len(self.raw_test_collections)} tests")
    #                 self.stack = [] ; self.steps = [] ; self.found = False
    #                 self.gen_one(self.start_place, must_cross)
    #                 if self.found == False:
    #                     print("EMERGENCY - HELP")
    #                 self.AEsteps = self.steps ; self.AEstack = self.stack
    #                 print(f"Random path length: {len(self.AEsteps)}")
    #                 return

    #             self.AEsteps = self.SAminsteps
    #             self.AEstack = self.SAminstack

    #     self.AEstack.append(node.name)
        
    # def calResem(self, a, b):
    #     if len(a) < len(b): #assume a longer
    #         a,b = b,a
    #     if len(b) == 0:
    #         return 0
    #     count = 0
    #     for i in b:
    #         if i in a:
    #             count += 1
        
    #     return count/len(b)        
    
    # def optimizer1(self, maxGreedy):
    #     self.visited = set()
    #     self.raw_test_collections = []
    #     self.test_collections = []
    #     for i in range(1,len(self.HList)):
    #         get_names = self.HList[i]
    #         random.shuffle(get_names)
    #         for name in get_names:
    #             if name not in self.visited:
    #                 self.start_to_A(name)
    #                 self.A_to_end(name, maxGreedy)
    #                 SE = self.AEstack
    #                 self.raw_test_collections.append(self.AEsteps)
    #                 for s in SE:
    #                     self.visited.add(s)

    #     #compare each test with each other
    #     trash = set()
    #     f = open(config.LOG_DIR + "test cases filtered.txt","w")
    #     for i in range(len(self.raw_test_collections)):
    #         for j in range(i+1,len(self.raw_test_collections)):
    #             rate = self.calResem(self.raw_test_collections[i],self.raw_test_collections[j])
    #             if rate > 0.99:
    #                 ii = False
    #                 if len(self.raw_test_collections[i]) < len(self.raw_test_collections[j]):
    #                     trash.add(i)
    #                     ii = True
    #                 else:
    #                     trash.add(j)
    #                 if ii:
    #                     f.write("Test case {0} - {1}    ".format(i+1,j+1))
    #                 else:
    #                     f.write("Test case {0} - {1}    ".format(j+1,i+1))
    #                 f.write("Resemblance rate: " + str(rate) + "\n")
    #     f.close()

    #     log = ""
    #     log += f"Total generated tests: {len(self.raw_test_collections)}\n"
    #     log += "Node coverage(place & trans): {0}/{1} = {2}\n".format(len(self.visited),len(self.recorder),len(self.visited)/len(self.recorder))
    #     log += f"Total generated tests (filtered): {len(self.raw_test_collections)- len(trash)}\n"

    #     #compare each test with each other (no assertions)
    #     self.to_test_collections()
    #     self.correct_test_steps()
    #     trash = set()
    #     f = open(config.LOG_DIR + "test cases filtered, no assert.txt","w")
    #     for i in range(len(self.test_collections)):
    #         for j in range(i+1,len(self.test_collections)):
    #             rate = self.calResem(self.test_collections[i],self.test_collections[j])
    #             if rate > 0.99:
    #                 ii = False
    #                 if len(self.test_collections[i]) < len(self.test_collections[j]):
    #                     trash.add(i)
    #                     ii = True
    #                 else:
    #                     trash.add(j)
    #                 if ii:
    #                     f.write("Test case {0} - {1}    ".format(i+1,j+1))
    #                 else:
    #                     f.write("Test case {0} - {1}    ".format(j+1,i+1))
    #                 f.write("Resemblance rate: " + str(rate) + "\n")
    #     f.close()

    #     log += f"Total generated tests (filtered, no assertions): {len(self.test_collections) - len(trash)}\n"
    #     self.test_collections = []
    #     return log
    
    def gen_one(self, node , must_cross = []):
        trans = False
        if len(node.name.split(";;;")) == 3:
            trans = True

        if not node.post.keys() and set(self.stack) >= set(must_cross):#dict empty -> end of test & cross required steps
            for i in range(len(self.raw_test_collections)): # avoid repeating generated tests in this iteration
                if self.compare_tcase(self.steps, self.raw_test_collections[i]):
                    return

            for i in range(len(self.exisiting_tests)): # avoid repeating tester test
                #convert = list(map(lambda x: x.split(";;;")[1] ,copy.deepcopy(self.steps))) #convert trans name to test steps
                if self.compare_tcase(self.steps, self.exisiting_tests[i]):
                    return

            for i in range(len(self.passed_tests)): # avoid repeating passed tests in previous iteration
                if self.compare_tcase(self.steps, self.passed_tests[i]):
                    return
                
            self.stack.append(node.name)
            self.found = True
            return
      
        if not self.is_valid_path(self.steps):
            return

        get_names = list(node.post.keys())
        random.shuffle(get_names)
        for name in get_names:
            if trans: #if this node is trans -> next node is place
                next_node = self.net._place[name]
            else:
                next_node = self.net._trans[name]
            
            #if (not trans and next_node.name not in self.steps) or trans: # if next is trans and already visited then skip
            if next_node.name not in self.stack and next_node.name not in self.skip_nodes:
                self.stack.append(node.name)
                if trans:
                    self.steps.append(node.name)

                self.gen_one(next_node , must_cross)
                if self.found:
                    return

                self.stack.pop()
                if trans:
                    self.steps.pop()

    def generate_suite(self):
        self.steps = []
        self.stack = []
        self.raw_test_collections = []
        self.test_collections = []
        self.visited = set()
        
        ret = ""
        for i in range(len(self.HList)-1,-1,-1):
            get_names = self.HList[i]
            random.shuffle(get_names)
            for name in get_names:
                if name not in self.visited and name not in self.skip_nodes:
                    self.steps = [] ; self.stack = []
                    self.found = False
                    self.gen_one(self.start_place,[name])
                    if not self.found:
                        self.skip_nodes.add(name)
                    else:
                        #add test to collection
                        self.raw_test_collections.append(copy.deepcopy(self.steps))
                        for s in self.stack:
                            self.visited.add(s)

        folder = config.FTEST_DIR
        with open(folder + "skipped.txt","w",encoding="utf8") as f:
            for i in self.skip_nodes:
                f.write(i + "\n")

        ret += f"Total generated tests: {len(self.raw_test_collections)}\n"
        ret += f"No. skipped nodes: {len(self.skip_nodes)}\n"
        ret += "Node coverage on graph (place & trans): {0}/{1} = {2}".format(len(self.visited),len(self.recorder),len(self.visited)/len(self.recorder))
        return ret

    def read_report(self, passed, failed):
        with open(config.ABS_DIR+"StateGraph/Data/assertion.txt") as f:
            raw = f.read()
        assertion = list(filter(lambda x: x != "", raw.split("\n")))
        with open(config.ABS_DIR+"StateGraph/Data/misc.txt") as f:
            raw = f.read()
        misc = list(filter(lambda x: x != "", raw.split("\n")))
        with open(config.ABS_DIR+"StateGraph/Data/skip.txt") as f:
            raw = f.read()
        skip = list(filter(lambda x: x != "", raw.split("\n")))
        def is_action(line):
            for a in assertion:
                if "WebUI." + a in line: return False
            for a in misc:
                if "WebUI." + a in line: return False
            for a in skip:
                if "WebUI." + a in line: return False
            return True

        def get_cnt(cur,maxc):
            res = str(cur)
            while len(res) < len(str(maxc)): #padding for better look
                res = "0" + res
            return res

        for i in range(len(passed)):
            self.passed_tests.append(copy.deepcopy(self.raw_test_collections[int(passed[i])]))
        
        for i in range(len(failed)):
            with open(config.OUTPUT_RAW_DIR + "Iter" + str(self.iter) + "/" + get_cnt(int(failed[i][0]),len(self.test_collections))+".groovy","r",encoding="utf8") as f:
                raw = f.read()
            lines = list(filter(lambda x: x != "", raw.split("\n")))
            filtered = list(filter(lambda x: x[:6] != "import", lines))
            # print("No import", len(filtered))
            # [print(i) for i in filtered]
            lines = copy.deepcopy(filtered[:failed[i][1]])
            # print("Real len", len(lines))
            # [print(i) for i in lines]
            fil1 = list(filter(lambda x: x[:11] != "WebUI.delay" and is_action(x) == True,lines))
            # print("Last filter", len(fil1))
            # [print(i) for i in fil1]
            test = copy.deepcopy(self.raw_test_collections[int(failed[i][0])])
            #[:2*len(fil1)+1]
            test = test[:len(fil1)]
            self.failed_tests.append(test)

        for i in range(len(self.failed_tests)-1,-1,-1): #filter duplicates
            for j in range(i-1,-1,-1):
                if self.failed_tests[i] == self.failed_tests[j]:
                    self.failed_tests.pop(j) ; print("F: Test filtered",j,"Test existed",i) ; break

        for i in range(len(self.passed_tests)-1,-1,-1): #filter duplicates
            for j in range(i-1,-1,-1):
                if self.passed_tests[i] == self.passed_tests[j]:
                    self.passed_tests.pop(j) ; print("P: Test filtered",j,"Test existed",i) ; break
        
        self.raw_test_collections = []
        self.test_collections = []

        self.visited = set()
        for tc in self.passed_tests:
            for step in tc:
                steps = step.split(";;;")
                self.visited.add(steps[0]) ; self.visited.add(steps[2]) #add place
                self.visited.add(step) #add trans
        
        visited = set()
        for i in range(len(self.passed_tests)-len(passed),len(self.passed_tests),1):
            for step in self.passed_tests[i]:
                steps = step.split(";;;")
                visited.add(steps[0]) ; visited.add(steps[2]) #add place
                visited.add(step) #add trans
        
        ret  = f"Number of passed test cases: {len(passed)}\n"
        ret += f"Number of failed test cases: {len(failed)}\n"
        ret += f"Total of passed test cases: {len(self.passed_tests)}\n"
        ret += f"Total of failed test cases: {len(self.failed_tests)}\n"
        ret += "Node coverage on execution (this iteration): {0}/{1} = {2}\n".format(len(visited),len(self.recorder),len(visited)/len(self.recorder))
        ret += "Node coverage on execution (all): {0}/{1} = {2}\n".format(len(self.visited),len(self.recorder),len(self.visited)/len(self.recorder))
        return ret, len(self.visited)/len(self.recorder)    

    # def temp(self):
    #     names = get_all_files(config.FTEST_DIR+"Pass/")
    #     names = names[:10]
    #     for name in names:
    #         with open(name,"r",encoding="utf8") as f:
    #             raw = f.read().split("\n")
    #             self.raw_test_collections.append(raw)


    #     self.publish()
    
    # def selfcollection_test(self):
    #     paths = get_all_files(config.OUTPUT_DIR)
    #     self.test_collections = []
    #     with open(config.ABS_DIR+"StateGraph/Data/action.txt") as f:
    #         raw_action = f.read()
    #     actions = list(filter(lambda x: x != "", raw_action.split("\n")))
    #     def is_action(line):
    #         for act in actions:
    #             if "WebUI." + act in line:
    #                 return True
    #         return False

    #     for path in paths:
    #         with open(path,"r") as f:
    #             data = f.read()
    #         lines = list(filter(lambda x: x != "", data.split("\n")))
    #         filtered = list(filter(lambda x: x[:6] != "import" and x[:11] != "WebUI.delay" and is_action(x) == True,lines))
    #         self.test_collections.append(filtered)