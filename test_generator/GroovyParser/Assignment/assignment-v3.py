import json
import glob
import os
read_path = "/home/thanh/Documents/GitHub/ISE-Implementation/GroovyParser/Output/*"
input_paths = glob.glob(read_path)
file_names = [os.path.basename(x) for x in input_paths]

def read_file(path):
    f = open(path,"r")
    strs = f.read().split("\n")
    f.close()
    return strs

const_lib = []
for i in range(4):
    const_lib.append([])

func_lib = []
for i in range(4):
    func_lib.append([])

all_func_lib = []

def string_val(x):
    return "'" + x + "'"

def substitute(json_obj,level,test_id):
    keep = []
    for i in range(len(json_obj)):
        #dfs
        if json_obj[i]["Child"]:
            child = substitute(json_obj[i]["Child"],level+1,test_id)
            func_lib[level+1] = []
            const_lib[level+1] = []
            json_obj[i]["Child"] = child

        #find and substitute
        tmp = json_obj[i]
        for lv in reversed(const_lib):
            for item in lv:
                lhs = item[0] ; rhs = item[1]
                if tmp["Receiver"] == lhs:
                    print("----------------ATTENTION-----------------")
                    print(tmp)
                    print("------------------------------------------")
                    tmp["Receiver"] = rhs
                
                for j in range(len(tmp["Input"])):
                    if tmp["Input"][j]["type"] == "Statement":
                        check = tmp["Input"][j]["code"]
                        pos = check.find(lhs["name"])
                        if pos != -1:
                            left = check[0:pos]
                            right = check[pos+len(lhs["name"]):]
                            if rhs["datatype"] == "class java.lang.String":
                                tmp["Input"][j]["code"] = left + string_val(rhs["value"]) + right
                            else:
                                tmp["Input"][j]["code"] = left + rhs["value"] + right

                    elif tmp["Input"][j]["type"] == "Variable":
                        if tmp["Input"][j]["name"] == lhs["name"]:
                            tmp["Input"][j] = rhs

        for lv in reversed(func_lib):
            for item in lv:
                lhs = item[0] ; rhs = item[1]
                if tmp["Receiver"] == lhs:
                    print("----------------ATTENTION-----------------")
                    print(tmp)
                    print("------------------------------------------")
                    tmp["Receiver"] = rhs
                
                for j in range(len(tmp["Input"])):
                    if tmp["Input"][j]["type"] == "Statement":
                        check = tmp["Input"][j]["code"]
                        pos = check.find(lhs)
                        if pos != -1:
                            left = check[0:pos]
                            right = check[pos+len(lhs):]
                            tmp["Input"][j]["code"] = left + rhs + right

                    elif tmp["Input"][j]["type"] == "Variable":
                        if tmp["Input"][j]["name"] == lhs:
                            tmp["Input"][j]["name"] = rhs
        
        #assignment check
        if tmp["Output"]:
            # const asssignment
            if tmp["Action"] == "Assignment":
                found = False
                if tmp["Output"][0]["type"] == "Variable" and tmp["Input"][0]["type"] == "Constant":
                    # check existing : exists ? update : add new
                    for lv in reversed(const_lib):
                        if found:
                            continue
                        for item in lv:
                            if tmp["Output"][0]["name"] == item[0]["name"]:
                                found = True
                                item[1] = tmp["Input"][0]
                                break

                if not found:
                    # add <name,const> to lib
                    if tmp["Output"][0]["type"] == "Variable" and tmp["Input"][0]["type"] == "Constant" and [tmp["Output"][0],tmp["Input"][0]] not in const_lib:
                        const_lib[level].append([tmp["Output"][0],tmp["Input"][0]])
                        continue
                    # found & updated variable name
                else:
                    continue

            # function assignment
            else:
                if tmp["Output"][0]["type"] == "Variable":
                    found = False
                    # check existing : exists ? update : add new
                    for lv in reversed(func_lib):
                        if found:
                            continue
                        for item in lv:
                            if tmp["Output"][0]["name"] == item[0]:
                                found = True
                                #update variable name
                                tmp["Output"][0]["name"] = item[1]

                                if [item[1],tmp] not in all_func_lib:
                                    all_func_lib.append([item[1],tmp])

                                break
                        
                    if not found:
                        newid=0
                        for item in func_lib[level]:
                            splitname = str(item[1]).split("_") 
                            if tmp["Action"] == splitname[0]:
                                newid = int(splitname[2])+1
                                break
                        newname = tmp["Action"]+ '_tc' +str(test_id)+ '_' + str(newid) +"_"+str(level)
                        
                        if [newname , tmp] not in all_func_lib:
                            all_func_lib.append([newname, tmp])
                        if [tmp["Output"][0]["name"], newname] not in func_lib[level]:
                            func_lib[level].append([tmp["Output"][0]["name"],newname])

                        tmp["Output"][0]["name"] = newname

        keep.append(tmp)

    return keep

def process(lines,i):
    ret = []
    for line in lines:
        #load json
        try:
            tmp = json.loads(line)
        except:
            continue

        ret.append(substitute([tmp],0,i))
    
    return ret

output = "/home/thanh/Documents/GitHub/ISE-Implementation/GroovyParser/Assignment/Output/"
prefix = "assignment_"
def write_file(content,id):
    f = open(output + prefix + file_names[id],"w")
    code = ""
    for sub in content:
        if sub == []:
            continue
        code += json.dumps(sub[0])
        code += "\n"
    f.write(code)
    f.close()

def write_file_log():
    f = open(output+"log.txt","w")
    code =""
    for item in all_func_lib:
        code += str(item)
        code += "\n"
    f.write(code)
    f.close()




#--------------------------run--------------------------
#   rename format: action + testcase id + reuse time(*) + nested level
#   reuse time(*): number of times the same variable is assigned with different values
for i in range(len(input_paths)):
    lines = read_file(input_paths[i])
    ret = process(lines,i)
    write_file(ret,i)
write_file_log()




