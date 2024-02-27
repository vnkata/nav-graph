import json
file_name = "test2.txt"
path = "/home/thanh/Documents/GitHub/ISE-Implementation/GroovyParser/Output/" + file_name
f = open(path,"r")
lines = f.read().split("\n")
f.close()
jsonobj = []
prev_tabs = 0
assignment_lib = []
for i in range(10):
    assignment_lib.append([])
#start substituting
for line in lines:
    tabs = 0; i = 0;
    while len(line) > 0 and  line[i] == '\t':
        tabs += 1; i += 1
    #load json
    try:
        tmp = json.loads(line)
    except:
        continue

    # scope reduced -> erase assignment 
    while prev_tabs > tabs:
        assignment_lib[prev_tabs] = []
        prev_tabs -= 1
    
    #find and substitute
    for lv in reversed(assignment_lib):
        for item in lv:
            lhs = item[0] ; rhs = item[1]
            if tmp["Receiver"] == lhs:
                tmp["Receiver"] = rhs
            
            try:
                check = tmp["Input"][0]["code"]
                pos = check.find(lhs)
                if pos != -1:
                    left = check[0:pos]
                    right = check[pos+len(lhs):]
                    tmp["Input"][0]["code"] = left + rhs + right
            except:
                dummy = 0       

    #assignment check
    if tmp["Output"]:
        found = False
        # check existing : exists ? update : add new
        for lv in reversed(assignment_lib):
            if found:
                continue
            for item in lv:
                if tmp["Output"][0]["name"] == item[0]:
                    found = True
                    if tmp["Action"] == "Assignment":
                        item[1] = tmp["Input"][0]["value"]
                    else:
                        code = tmp["Receiver"] + "." + tmp["Action"] + "(" + tmp["Input"][0]["code"] + ")"
                        item[1] = code
                    break

        if not found:
            # assign const val
            if tmp["Action"] == "Assignment":
                if tmp["Output"][0]["type"] == "Variable" and tmp["Input"][0]["type"] == "Constant":
                    assignment_lib[tabs].append([tmp["Output"][0]["name"],tmp["Input"][0]["value"]])
                else:
                    jsonobj.append([tmp,tabs])        

            # assign code
            else:
                if tmp["Output"][0]["type"] == "Variable":
                    rhs = tmp["Receiver"] + "." + tmp["Action"] + "("
                    input = tmp['Input']
                    for j in range(len(input)):
                        in_type = input[j]['type']
                        if in_type == 'Constant':
                            #const is string -> add quotes
                            if input[j]['datatype'] == 'java.lang.String':
                                rhs += "'" + input[j]['value'] + "'"
                            else:
                                rhs += input[j]['value']
                        elif in_type == 'Statement':
                            rhs += input[j]['code']
                        elif in_type == 'Variable':
                            #var is string -> add quotes
                            if input[j]['datatype'] == 'java.lang.String':
                                rhs += "'" + input[j]['name'] + "'"
                            else:
                                rhs += input[j]['name']    
                        
                        if j + 1 != len(input):
                            rhs += ', '
                    rhs += ')'
                    assignment_lib[tabs].append([tmp["Output"][0]["name"],rhs])
                else:
                    jsonobj.append([tmp,tabs])        

        # skip assingment steps
        prev_tabs = tabs
        continue

    jsonobj.append([tmp,tabs])        
    prev_tabs = tabs

prefix = "GroovyParser/Assignment/Output/assignment-v2_"
f = open(prefix + file_name,"w")
for obj in jsonobj:
    line = "" ; i = 0
    while i < obj[1]:
        line += "\t"
        i += 1
    line += json.dumps(obj[0])
    line += "\n"
    f.write(line)

f.close()