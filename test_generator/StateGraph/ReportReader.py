import config
import os

class ReportReader:
    def __init__(self, report_dir, session) -> None:
        raw = None
        with open(report_dir, "r") as f:
            raw = f.read()
        
        self.report = list(filter(lambda x: x != "", raw.split("\n")))
        for i in range(len(self.report)):
            self.report[i] = self.report[i].split(",")

        self.session = session

    def summarize(self):
        #return a failed list, each ele has test number and number of failed steps [[001,10]]
        failed = [] ; fail_cnt = 0 ; error_cnt = 0
        #return a passed list, each ele has test number [002, 003]
        passed = []; pass_cnt = 0
        for i in  range(len(self.report)):
            if "Test Cases/" + self.session in self.report[i][0]:
                lis = self.report[i][0].split("_")
                num = lis[-1]
                if self.report[i][7] == "PASSED": #passed test case
                    passed.append(num) ; pass_cnt += 1
                elif self.report[i][7] == "FAILED": #failed test case (failed to execute action)
                    pac = [num]
                    cnt = 0
                    stop = False
                    for j in range(i+1,len(self.report)):
                        cnt += 1
                        for k in self.report[j]:
                            if k == "FAILED":
                                stop = True
                                break
                        if stop:
                            break
                    pac.append(cnt)
                    failed.append(pac) ; fail_cnt += 1
                elif self.report[i][7] == "ERROR": #failed test case (failed to execute assertion)
                    pac = [num]
                    cnt = 0
                    stop = False
                    for j in range(i+1,len(self.report)):
                        cnt += 1
                        for k in self.report[j]:
                            if k == "ERROR":
                                stop = True
                                break
                        if stop:
                            break
                    pac.append(cnt)
                    failed.append(pac) ; error_cnt += 1
        
        print("Number of error tests:", error_cnt)
        return passed,failed