import re
import json

katalonPath = "C:\\Users\\Prometheus\\Downloads\\moodle-14\\Test Automation - SE Bonus"
#selfHealing = katalonPath + "\\Reports\\Iteration15_20220117_230729\\Run All Test Cases\\20220117_230729"
selfHealing = katalonPath + "\\Reports\\Self-healing"
selfHealing += "\\" + "broken-test-objects.json"

def readBroken(path):
    f = open(path,encoding="utf8")
    potentialFix = json.load(f)
    f.close()
    return potentialFix

def processBroken(potentialFix):
    for obj in potentialFix["brokenTestObjects"]:
        # if self-healing on the object is approved -> fix
        # only fix XPATH attribute for now!
        if "approved" in obj and obj["approved"] and (obj["proposedLocatorMethod"] == "XPATH"):
            # build object path
            rawPath = obj["testObjectId"].split("/")
            rawPath = "\\".join(rawPath)
            objPath = katalonPath + "\\" + rawPath + ".rs"

            # open file & change data
            try:    
                with open(objPath, encoding="utf8") as f:
                    brokenObj = f.read()
            except:
                continue

            lines = brokenObj.split("\n")
            for i in range(len(lines)):
                if "<key>XPATH</key>" in lines[i]:
                    fix = lines[i+1]
                    s = fix.find("<value>")
                    e = fix.find("</value>")
                    fix = fix[:s+7] + obj["proposedLocator"] + fix[e:]
                    lines[i+1] = fix
                    break

            # bsData = BeautifulSoup(brokenObj,"xml")

            # keys = bsData.find_all("key")
            # for k in keys:
            #     if k.text == "XPATH":
            #         siblings = list(k.next_siblings)
            #         for s in siblings:
            #             if isinstance(s, bs4.element.Tag) and s.name == "value":
            #                 #print("cur: ", s.text)
            #                 #print("fix: ", obj["proposedLocator"])
            #                 s.string = obj["proposedLocator"]

            # overwrite data
            #tmp = katalonPath + "\\" + rawPath + "test.rs"
            #print(objPath)
            with open(objPath,"w",encoding="utf8") as f:
                #f.write(bsData.prettify())
                lines = "\n".join(lines)
                f.write(lines)
                

processBroken(readBroken(selfHealing))


