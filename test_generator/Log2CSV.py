import config
import glob
import re

pattern = config.LOG_DIR + "*run_log.txt"
path = glob.glob(pattern, recursive=True)
with open(path[0],"r",encoding="utf8") as f:
    raw = f.read().split("\n")

def get_num(text):
    return re.findall("[0-9]+(?:[\:\.\/]*[0-9]+)*",text)

i = 0
res = []
while i < len(raw):
    if "Generating starts at" in raw[i]: #start of an iteration
        j = i + 1
        total = ""; skip = ""; gcoverage = ""; ecoverage ="";ecoveragenow =""; gentime =""; etime =""; report = ""; p =""; f="";pall="";fall=""
        while j < len(raw):
            if "Total generated tests" in raw[j]:
                total = get_num(raw[j])[0]
            elif "No. skipped nodes:" in raw[j]:
                skip = get_num(raw[j])[0]
            elif "Node coverage on graph (place & trans)" in raw[j]:
                gcoverage = get_num(raw[j])[1]
            elif "Generating took" in raw[j]:
                gentime = get_num(raw[j])[0]
            elif "Test execution took" in raw[j]:
                etime = get_num(raw[j])[0]
            elif "Expect reports" in raw[j]:
                report = re.sub("Expect reports at:","",raw[j])
            elif "Number of passed" in raw[j]:
                p = get_num(raw[j])[0]
            elif "Number of failed" in raw[j]:
                f = get_num(raw[j])[0]
            elif "Total of passed" in raw[j]:
                pall = get_num(raw[j])[0]
            elif "Total of failed" in raw[j]:
                fall = get_num(raw[j])[0]
            elif "Node coverage on execution (this iteration)" in raw[j]:
                ecoveragenow = get_num(raw[j])[1]
            elif "Node coverage on execution (all)" in raw[j]:
                ecoverage = get_num(raw[j])[1]
                break
            j += 1
        i = j
        res.append([skip,total,gentime,etime,p,f,pall,fall,gcoverage,ecoveragenow,ecoverage,report])
    i += 1

with open(config.ABS_DIR +"report.csv","w",encoding="utf8") as f:
    f.write("No. skipped nodes, Generated tests, Generation time, Execution time, No. executable tests, No. non-executable tests, No. total executable tests, No. total non-executable tests, Coverage (on net), Coverage (on execution - this iter), Coverage (on execution - now), Report location\n")
    for i in res:
        f.write(",".join(i)+"\n")
