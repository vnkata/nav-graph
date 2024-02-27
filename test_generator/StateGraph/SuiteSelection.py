import copy
from math import sqrt
import random
import numpy as np
import config
from os.path import isfile, join
import os
import matplotlib.pyplot as plt


def get_all_files(dir_path):
    return [join(dir_path, f) for f in os.listdir(dir_path) if isfile(join(dir_path, f))]

class SuiteSelection:
    def __init__(self, suite_folder= config.FTEST_DIR) -> None:
        self.test_collections = []
        self.ori_test_collections = []
        
        names = get_all_files(suite_folder + "Pass/")
        for name in names:
            with open(name,"r",encoding="utf8") as f:
                self.test_collections.append(f.read().split("\n"))
            
        if suite_folder == config.ABS_DIR + "Moodle_29_act+asrt/": #-323 pass at convergence
            self.test_collections= self.test_collections[:323]

        names = get_all_files(suite_folder + "Original/")
        for name in names:
            with open(name,"r",encoding="utf8") as f:
                self.ori_test_collections.append(f.read().split("\n"))

        self.total_test_collections = self.ori_test_collections + self.test_collections

        #print("Original test cases has", len(self.ori_test_collections))

        self.appearances_dict = {}
        for test in self.test_collections:
            for step in test:
                if step in self.appearances_dict.keys(): #update existing
                    self.appearances_dict[step] += 1
                else: #update new record
                    self.appearances_dict.update({step:1})

        self.ori_appearances_dict = {}
        for test in self.ori_test_collections:
            for step in test:
                if step in self.appearances_dict.keys(): #update existing
                    self.appearances_dict[step] += 1
                else: #update new record
                    self.appearances_dict.update({step:1})

            for step in test:
                if step in self.ori_appearances_dict.keys(): #update existing
                    self.ori_appearances_dict[step] += 1
                else: #update new record
                    self.ori_appearances_dict.update({step:1})

        #print(len(self.appearances_dict))
        #[print(i,self.appearances_dict[i]) for i in self.appearances_dict]


    def score_test(self, test):
        val = 0
        for step in test:
            if step in self.visited:
                continue #no value
            else:
                val += 1/self.appearances_dict[step]
        return val
    
    def optimizer1(self, ori_pen = 0, display = True, top = 1):
        self.visited = set()
        self.chosen = []
        
        tester = 0
        stop = False
        while True:
            grade = []
            i = 0
            for test in self.test_collections:
                grade.append([self.score_test(test),i])
                i+=1
            for test in self.ori_test_collections:
                grade.append([self.score_test(test)-ori_pen,i])
                i+=1

            grade.sort(reverse=True)
            stop = True
            for i in range(top):
                if grade[i][0] != 0:
                    stop = False
            if stop:
                break

            chosen_idx = None
            tmp = grade[:top]
            tmp = list(filter(lambda x: x[0] != 0,tmp))
            chosen_idx = random.randint(0,len(tmp)-1)    
            
            if grade[chosen_idx][1] < len(self.test_collections):
                self.chosen.append(self.test_collections[grade[chosen_idx][1]])
            else:
                tester += 1
                self.chosen.append(self.ori_test_collections[grade[chosen_idx][1]-len(self.test_collections)])

            for step in self.chosen[-1]:
                self.visited.add(step)

        if display:
            print("Coverage:" , len(self.visited), "/",len(self.appearances_dict))
            print("Number of test cases:", len(self.chosen))
            print("Number of test cases in original suite:", tester,"\n")

            self.suite_stat(self.ori_test_collections,"Original test suite")
            if ori_pen == 0:
                self.suite_stat(self.chosen, "Goal (1) test suite")
            else:
                self.suite_stat(self.chosen, f"Goal (1) test suite with penalty {ori_pen}")

        return len(self.visited),len(self.appearances_dict), len(self.chosen) , tester

    def optimizer1_1(self, ori_pen = 0, display = True, top = 1):
        self.visited = set()
        self.chosen = []
        
        tester = 0
        stop = False
        while True:
            grade = []
            i = 0
            for test in self.test_collections:
                grade.append([self.score_test(test),1/len(test),i])
                i+=1
            for test in self.ori_test_collections:
                grade.append([self.score_test(test)-ori_pen,1/len(test),i])
                i+=1

            grade.sort(reverse=True)
            stop = True
            for i in range(top):
                if grade[i][0] != 0:
                    stop = False
            if stop:
                break

            chosen_idx = None
            tmp = grade[:top]
            tmp = list(filter(lambda x: x[0] != 0,tmp))
            chosen_idx = random.randint(0,len(tmp)-1)    
            
            if grade[chosen_idx][2] < len(self.test_collections):
                self.chosen.append(self.test_collections[grade[chosen_idx][2]])
            else:
                tester += 1
                self.chosen.append(self.ori_test_collections[grade[chosen_idx][2]-len(self.test_collections)])

            for step in self.chosen[-1]:
                self.visited.add(step)

        if display:
            print("Coverage:" , len(self.visited), "/",len(self.appearances_dict))
            print("Number of test cases:", len(self.chosen))
            print("Number of test cases in original suite:", tester,"\n")

            self.suite_stat(self.ori_test_collections,"Original test suite")
            if ori_pen == 0:
                self.suite_stat(self.chosen, "Goal (5) test suite")
            else:
                self.suite_stat(self.chosen, f"Goal (1) test suite with penalty {ori_pen}")

        return len(self.visited),len(self.appearances_dict), len(self.chosen) , tester

    def tabu_search(self, eval_func, debug = False, max_iter = 100, drop_rate = 30, top = 1):
        """ OPTIMIZE GOAL 1 """
        def find_suite(test_collections, idx, chosen):
            visited = set() ; s = []
            for i in chosen:
                for step in test_collections[i]:
                    visited.add(step)
            random.shuffle(idx)
            for i in idx:
                add = False
                for step in test_collections[i]:
                    if step not in visited:
                        add = True ; break
                if add:
                    s.append(i)
                    for step in test_collections[i]:
                        visited.add(step)
                if len(visited) == len(self.appearances_dict):
                    break
            return chosen + s

        def grade_test(test, visited):
            cnt = 0
            for step in test:
                if step not in visited:
                    cnt += 1
            return cnt

        def find_greedy_suite(test_collections, idx, chosen):
            self.visited = set() ; s = [] ; tests = []
            for i in chosen:
                for step in test_collections[i]:
                    self.visited.add(step)
            
            while True:
                grade = []
                i = 0
                for test in test_collections:
                    grade.append([grade_test(test,self.visited),i])
                    i+=1

                grade.sort(reverse=True)
                if grade[0][0] == 0: #all nodes covered
                    break
                chosen_idx = 0

                s.append(grade[chosen_idx][1])
                tests.append(test_collections[s[-1]])

                for step in tests[-1]:
                    self.visited.add(step)
            
            return chosen + s

        def evaluate_min(sol):
            return len(sol)

        def evaluate_bal(sol):
            s = list(map(lambda x: self.total_test_collections[x],sol))
            _, stddev = self.suite_stat(s, "", False)
            return round(stddev,3)

        def evaluate_dup(sol):
            s = list(map(lambda x: self.total_test_collections[x],sol))
            return sum([len(x) for x in s])

        def is_better(sol1, sol2):
            res1 = evalcall[eval_func](sol1) ; res2 = evalcall[eval_func](sol2)
            return res1 <= res2, f"now {res1} - best {res2}"

        # def evaluate(sol):
        #     s = list(map(lambda x: self.total_test_collections[x],sol))
        #     _, stddev = self.suite_stat(s, "", False)
        #     return len(sol), round(stddev,3)

        # def is_better(sol1, sol2):
        #     if len(sol1) > len(sol2):
        #         return False, ""
        #     elif len(sol1) == len(sol2):
        #         s1 = list(map(lambda x: self.total_test_collections[x],sol1))
        #         s2 = list(map(lambda x: self.total_test_collections[x],sol2))
        #         _, stddev1 = self.suite_stat(s1, "",False)
        #         _, stddev2 = self.suite_stat(s2, "", False)
        #         return round(stddev1,3) < round(stddev2,3), f" now {len(sol1)} - best {len(sol2)} \n now {round(stddev1,3)} - best {round(stddev2,3)}"
        #     elif len(sol1) < len(sol2):
        #         return True, f" now {len(sol1)} - best {len(sol2)}"

        """ Find initial solution """
        evalcall = { 'minimal' : evaluate_min, 'balance' : evaluate_bal , 'duplicate' : evaluate_dup}
        test_collections = self.ori_test_collections + self.test_collections
        idx = np.arange(0,len(test_collections),1)
        random.shuffle(idx)
        s0 = find_suite(test_collections,idx,[])
        #s0 = list(np.arange(0,len(self.ori_test_collections),1))

        sBest = s0
        bestCandidate = [s0]
        tabuList = []
        tabuList.append(s0)

        """Start iteration to find the best solution"""
        MAX_ITER = max_iter ; DROP_RATE = drop_rate ; MAX_TABU_SIZE = MAX_ITER*top
        if debug:
            print("Tabu search settings")
            print("Optimization function:", eval_func)
            print("Max iteration:", MAX_ITER)
            print("Drop rate:", DROP_RATE)
            print("Top neighbor(s):", top)
        for i in range(MAX_ITER):
            """Get neighbor solutions"""
            neighborSols = []
            for k in range(len(bestCandidate)):
                for j in range(DROP_RATE):
                    tmp = copy.deepcopy(bestCandidate[k])
                    random.shuffle(tmp)
                    tmpCandidate = tmp[:int(len(tmp)*(1-DROP_RATE/100))]
                    s = find_suite(test_collections,idx,tmpCandidate)
                    neighborSols.append(s)

            neighborSols = list(map(lambda x: (x,evalcall[eval_func](x)),neighborSols))
            neighborSols.sort(key= lambda x: x[1])
            bestCandidate = neighborSols[:top]
            bestCandidate = list(map(lambda x: x[0],bestCandidate))
            
            res, msg = is_better(bestCandidate[0], sBest)
            if res:
                if debug:
                    print("Best solution found at iteration", i)
                    print(msg,flush=True)
                sBest = bestCandidate[0]

            tabuList.append(bestCandidate[0])
            if len(tabuList) > MAX_TABU_SIZE:
                tabuList.pop(0) #delete the oldest

        chosen = [] ; tester = 0
        for i in sBest:
            chosen.append(test_collections[i])
            if i < len(self.ori_test_collections):
                tester += 1            

        if debug:
            print("Number of test cases:", len(chosen))
            print("Number of test cases in original suite:", tester,"\n")

            #self.suite_stat(self.ori_test_collections,"Original test suite")
            self.suite_stat(chosen, "Tabu search test suite")

        return len(chosen), tester, evalcall[eval_func](sBest), evalcall[eval_func]([i for i in range(len(self.ori_test_collections))])
        

    def opti1_pen_learn(self, alpha = 1,bias = 1):
        l = 0
        #find the max right without hurting coverage
        r = alpha
        while True:
            c, maxc, suite_len, tester = self.optimizer1(r,False)
            if c < maxc: break
            r += alpha

        best_pen= None; _, __, best_len, best_tester = self.optimizer1(l,False)
        mid = float(l*bias+r)/(bias+1)
        while True:
            #print("Trying with pen",l)
            lc,lmaxc,l_len,l_tester = self.optimizer1(l,False)
            #print("Trying with pen",r)
            rc,rmaxc,r_len,r_tester = self.optimizer1(r,False)

            if rc < rmaxc:
                r = mid
            else:
                if l_tester < best_tester:
                    best_tester = l_tester ; r = mid
                    best_pen = l
                elif r_tester < best_tester:
                    best_tester = r_tester ; l = mid
                    best_pen = r
                else:
                    if l_len <= best_len and l_len < r_len:
                        r = mid ; best_len = l_len ; best_pen = l
                    elif r_len <= best_len and r_len < l_len:
                        l = mid ; best_len = r_len ; best_pen = r         

            if round(mid,4) == round(float(l*bias+r)/(bias+1),4):
                break
            mid = float(l*bias+r)/(bias+1)

        print("Best penalty for the selection:",best_pen)
        self.optimizer1(best_pen)

    def optimizer2(self, display = False):
        self.visited = set()
        self.chosen = []
        
        anchor = sum(list(map(lambda x: len(x),self.total_test_collections)))/len(self.total_test_collections)
        def grade_tc(tc,anc):
            val = 0
            for step in tc:
                if step not in self.visited:
                    val += 1; break
            return 0 if val == 0 else 1/abs(len(tc)-anc)

        sBest = [] ; sdBest = float('inf')
        for i in range(-40,40):
            anc = anchor + i/4
            tester = 0
            self.visited = set()
            self.chosen= []
            while len(self.visited) < len(self.appearances_dict):
                grade = []
                i = 0
                for test in self.total_test_collections:
                    grade.append([grade_tc(test,anc),self.score_test(test),i])
                    i+=1

                grade.sort(reverse=True)
                
                self.chosen.append(self.total_test_collections[grade[0][2]])
                if grade[0][2] < len(self.ori_test_collections):
                    tester += 1

                for step in self.chosen[-1]:
                    self.visited.add(step)

            _, stddev = self.suite_stat(self.chosen,"",False)
            if sBest == [] or round(stddev,4) < round(sdBest, 4):
                sBest = self.chosen ; sdBest = stddev

        if display:
            print("Coverage:" , len(self.visited), "/",len(self.appearances_dict))
            print("Number of test cases:", len(sBest))
            print("Number of test cases in original suite:", tester,"\n")

            self.suite_stat(self.ori_test_collections,"Original test suite")
            self.suite_stat(sBest, "Balance test suite (Goal 2)")

        return len(self.visited),len(self.appearances_dict), len(sBest) , tester


    def optimizer3(self):
        self.test_score = {}
        self.visited = set()
        self.chosen = []
        
        tester = 0
        while True:
            grade = []
            i = 0
            for test in self.test_collections:
                grade.append([self.score_test(test),i])
                i+=1
            grade.sort(reverse=True)
            if grade[0][0] == 0: #no test gives coverage
                break
            
            self.chosen.append(self.test_collections[grade[0][1]])

            for step in self.chosen[-1]:
                self.visited.add(step)

        tester = 0
        while True:
            grade = []
            i = 0
            for test in self.ori_test_collections:
                grade.append([self.score_test(test),i])
                i+=1
            grade.sort(reverse=True)
            if grade[0][0] == 0: #no test gives coverage
                break
            
            tester += 1 
            self.chosen.append(self.ori_test_collections[grade[0][1]])

            for step in self.chosen[-1]:
                self.visited.add(step)

        print("Number of trans:" , len(self.appearances_dict))
        print("Number of covered trans:", len(self.visited))
        print("Number of test cases:", len(self.chosen))
        print("Number of test cases in original suite:", tester)

        self.suite_stat(self.ori_test_collections,"Original test suite")
        self.suite_stat(self.chosen, "Goal (3) test suite")

    def cal_resemblance(self, gen, src):
        cnt = 0
        for step in gen:
            if step in src:
                cnt += 1
        return cnt/len(gen)
    
    def optimizer4(self):
        rate_list = {}
        for i in range(len(self.test_collections)):
            max_rate = 0
            for j in range(len(self.ori_test_collections)):
                rate = self.cal_resemblance(self.test_collections[i],self.ori_test_collections[j])
                max_rate = max(rate,max_rate)
            rate_list.update({i:max_rate})

        range_cnt = 20
        bins = []
        for i in range(range_cnt):
            bins.append([i/range_cnt,0])

        for i in rate_list.keys():
            for j in range(len(bins)):
                if rate_list[i] <= bins[j][0]:
                    bins[j][1] += 1
        
        [print(i) for i in bins]
        data = list(map(list, zip(*bins))) #transpose list of lists
        plt.plot(data[0], data[1])
        plt.title('Resemblance rate vs Count')
        plt.xlabel('Resemblance rate')
        plt.ylabel('Count')
        plt.show() 

    def optimizer5(self):
        # get all test
        # cal average step avg
        # grade test: sum of all step val
        # step val = agv - step_freq
        # remove test with highest point without hurting the coverage
        # repeat until no test yields positive points
        test_suite = copy.deepcopy(self.test_collections)
        test_suite += copy.deepcopy(self.ori_test_collections)
        freq_dict = copy.deepcopy(self.appearances_dict)
        
        #max_len = max([len(test) for test in test_suite])
        #min_len = min([len(test) for test in test_suite])

        while True:
            rank = []
            sumf = sum([freq_dict[i] for i in freq_dict.keys()])
            avg = sumf/len(freq_dict)

            for i in range(len(test_suite)):
                score = 0
                for step in test_suite[i]:
                    if step in freq_dict.keys():
                        if freq_dict[step] == 1: #hurt coverage if picked
                            score = 0; break
                        score += avg - freq_dict[step]

                if score < 0:
                    rank.append([score,i])
                
            if len(rank) == 0: break
            rank.sort()
            
            for step in test_suite[rank[0][1]]: #reduce all steps
                freq_dict[step] -= 1
            test_suite.pop(rank[0][1]) #pop test with highest score

        data1 = []
        for i in freq_dict.keys():
            data1.append(freq_dict[i])
        data1.sort()

        data2 = []
        for i in self.ori_appearances_dict.keys():
            data2.append(self.ori_appearances_dict[i])
        data2.sort()

        cnt = 0
        for i in data1:
            cnt += 1
            plt.scatter(cnt, i*len(self.ori_test_collections)/len(test_suite), color='red', marker='o')

        cnt = 0
        for i in data2:
            cnt += 1
            plt.scatter(cnt, i, color='blue', marker='x')

        #plt.plot(data1[0], data1[1] , color='red', marker='o')
        #plt.plot(data2[0], data2[1] , color='blue', marker='x')
        plt.title(f'Test step frequency', fontsize=14)
        plt.xlabel('', fontsize=14)
        plt.ylabel(f'Test step frequency', fontsize=14)
        plt.grid(True)
        plt.show()
        self.suite_stat(self.ori_test_collections,"Original test suite")

        tester = 0
        for i in test_suite:
            if i in self.ori_test_collections:
                tester += 1

        print("No. test cases", len(test_suite))
        print("No. original test cases", tester) 
        self.suite_stat(test_suite, "Less duplicate test steps suite")

    def suite_stat(self,suite,suite_name = "",display=True):
        step_mean = 0
        step_std_dev = 0

        mod = list(map(lambda x: len(x),suite))
        step_mean = sum(mod)/len(suite)

        def cal_dist(x, y):
            return (len(x)-y)*(len(x)-y)
        modd = list(map(lambda x: cal_dist(x,step_mean),suite))
        step_std_dev = sqrt(sum(modd)/len(suite))

        if display:
            print(suite_name)
            print("Total steps:", sum(mod))
            print("Step mean:", step_mean)
            print("Step std. dev:", step_std_dev,"\n")
        
        return step_mean, step_std_dev