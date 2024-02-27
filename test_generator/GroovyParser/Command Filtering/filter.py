import json

#read commands filter from file
cmdpath = "/home/thanh/Documents/GitHub/ISE-Implementation/StateGraph/Data/"
action = "action.txt"
assertion = "assertion.txt"
f = open(cmdpath + action,"r")
actionlib = f.read().split("\n") ; f.close()
f = open(cmdpath + assertion, "r")
assertlib = f.read().split("\n") ; f.close()

#read test scripts from file
file_name = "input.txt"
path = "/home/thanh/Documents/GitHub/ISE-Implementation/GroovyParser/Assignment/Output/assignment-v2_" + file_name
f = open(path,"r")
lines = f.read().split("\n") ; f.close()
jsonobj = [] ; tabs = 0

for line in lines:
    tabs = 0; i = 0
    while len(line) > 0 and  line[i] == '\t':
        tabs += 1; i += 1

    #load json
    try:
        tmp = json.loads(line)
    except:
        continue

    if tmp['Receiver']:
        #assignment
        if tmp['Output']:
            dummy = 1
        #check WebUI commands
        else:
            if tmp['Receiver'] == "WebUI":
                cmd = tmp['Action']
                found = False
                for actcmd in actionlib:
                    if cmd == actcmd:
                        tmp.update({"cmdtype":'action'})
                        jsonobj.append([tmp,tabs])
                        found = True
                        break
                if found:
                    continue
                else:
                    for astcmd in assertlib:
                        if cmd == astcmd:
                            tmp.update({"cmdtype":'action'})
                            jsonobj.append([tmp,tabs])
                            found = True
                            break
                    if found:
                        continue
        
    tmp.update({"cmdtype": 'other'})
    jsonobj.append([tmp,tabs])

prefix = "GroovyParser/Command Filtering/Output/"
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
