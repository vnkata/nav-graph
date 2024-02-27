import json
path = "/home/thanh/Documents/GitHub/ISE-Implementation/GroovyParser/Output/test2.txt"
f = open(path,"r")
lines = f.read().split("\n")
jsonobj = []
row = 0 ; prev_tabs = 0
tabs_arr = []
tabs_lib = []
for i in range(10):
    tabs_arr.append(-1)
    tabs_lib.append([])
#load json obj and index {} positions
for line in lines:
    tabs = 0; i = 0; row += 1
    while len(line) > 0 and  line[i] == '\t':
        tabs += 1; i += 1
    #tabs < prev_tabs -> must be a close }
    while prev_tabs > tabs:
        tabs_lib[prev_tabs].append([tabs_arr[prev_tabs],row])
        tabs_arr[prev_tabs] = -1
        prev_tabs -= 1 
    #mark tabs
    for j in range(tabs+1):
        if tabs_arr[j] == -1:
            tabs_arr[j] = row
    try:
        y = json.loads(line)
        #public assignment
        if tabs == 0:
            jsonobj.append([y,-1])
        #local assignment
        else:
            jsonobj.append([y,tabs])
    except:
        dummy = 0
    prev_tabs = tabs

#print tabs info
for item in tabs_lib:
    print(item)

library = []
#indexing scope and content of assignment
for item in jsonobj:
    obj = item[0]
    if obj["Output"]:
        if obj["Action"] == "Assignment":
            library.append([obj["Output"][0]["name"],obj["Input"][0]["value"],item[1]])
        else:
            code = obj["Receiver"] + "." + obj["Action"] + "(" + obj["Input"][0]["code"] + ")"
            if [obj["Output"][0]["name"],code,item[1]] not in library:
                library.append([obj["Output"][0]["name"],code,item[1]])

#print assignment info
for item in library:
    print(item)