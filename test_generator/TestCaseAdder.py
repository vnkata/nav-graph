import os
from os.path import isfile, join
import config
import rstr
import copy
import shutil
import datetime
import re

"""
Assumption: Folder OutputGroovy/ exists and contains only .groovy files
"""

def get_all_files(dir_path):
    return [join(dir_path, f) for f in os.listdir(dir_path) if isfile(join(dir_path, f))]

class TestAdder:
    def __init__(self) -> None:
        self.init_data()

    def self_check(self):
        self.groovyScripts = get_all_files(config.OUTPUT_DIR)
        if self.groovyScripts == []:
            print("""Warning: folder OutputGroovy is empty""")
            self.sessionID = None
            return
        
        now = datetime.datetime.now()
        self.session = "_" + now.strftime("%y_%b_%d_%a_%H_%M_%S")
        self.sessionID = self.session
        print("Session ID: ", self.sessionID)

        self.cnt = 0
        self.iter = 0
        self.brainWashed()
    
    def brainWashed(self):
        #rename all files in OutputGroovy/
        victims = get_all_files(config.OUTPUT_DIR)
        for v in victims:
            clone = re.sub('[^0-9]',"",v)
            num = 13 - len(clone)
            pattern = "[0-9]{" + f"{num}" + "}"
            os.rename(v,"OutputGroovy/"+"Script"+clone+self.generate_KID(pattern)+".groovy")
        self.groovyScripts = get_all_files(config.OUTPUT_DIR)
        

    def run(self):
        if self.groovyScripts == []:
            return
        self.hackScripts()
        self.hackTestCases()
        self.hackTestSuites()

    def cleanTrace(self):
        log = ""
        if self.groovyScripts == []:
            return
        log += self.removeScripts()
        log += self.removeTestCases()
        log += self.removeTestSuites()
        return log
            
    def next_count(self, max_count):
        res = str(self.cnt)
        while len(res) < len(str(max_count)): #padding for better look
            res = "0" + res
        self.cnt += 1
        return res

    def next_iter(self):
        self.iter += 1
        res = str(self.iter)
        while len(res) < 3:
            res = "0" + res
        return "Iter" + res

    def generate_KID(self, pattern):
        generated = rstr.xeger(pattern)
        return generated

    def hackScripts(self):
        path = config.KATALON_DIR + "Scripts/"
        # create folder with generated name(self.sessionID + self.next_count) & copy .groovy file to created folder
        self.groovyScrpName = []
        for s in self.groovyScripts:
            store = self.sessionID + "_" + self.next_count(len(self.groovyScripts))
            subpath = path + store + "/"
            try:
                os.makedirs(subpath)
                shutil.copy(s, subpath)
                self.groovyScrpName.append(store)
            except FileExistsError:
                print("Directory " , subpath ,  " already exists")
                continue

    def removeScripts(self):
        log = ""
        path = config.KATALON_DIR + "Scripts/"
        for s in self.groovyScrpName:
            try:
                shutil.rmtree(path + s)
                log += f"Removed {path+ s}\n"
            except FileExistsError:
                print("Directory" , path + s ,  "not exists")
                continue
        return log

    def fill_TC(self,name, guid):
        template = copy.deepcopy(self.tcsample)
        res = template.format(name,guid)
        return res

    def hackTestCases(self):
        #name               must be the same with folder name generated in hackScripts
        #.tc name           is the same as name
        #testCaseGuid       is generated with format:
        #    [a-f0-9]{8}-{4}-{4}-{4}-{12}
        path = config.KATALON_DIR + "Test Cases/"
        self.generatedTCGUID = []
        for scrp in self.groovyScrpName:
            guid = self.generate_KID(self.GUID)
            try:
                with open(path+scrp+".tc","w") as f:
                    f.write(self.fill_TC(scrp,guid))
                self.fill_TC(scrp,guid)
                self.generatedTCGUID.append(guid)
            except:
                print("File", path+scrp+".tc","could not be opened")
                continue

    def removeTestCases(self):
        log = ""
        path = config.KATALON_DIR + "Test Cases/"
        for name in self.groovyScrpName:
            try:
                os.remove(path + name+".tc")
                log += f"Removed {path + name +'.tc'}\n"
            except:
                print("File", path+ name +".tc","not exists")
                continue
        return log

    def hackTestSuites(self):
        #create {test suite name}.groovy with format
        path = config.KATALON_DIR + "Test Suites/"
        try:
            with open(path + self.sessionID + ".groovy","w") as f:
                f.write(self.tsgroovy)
        except:
            print("File", path + self.sessionID + ".groovy", "could not be opened")
        #create {test suite name}.ts with format
        #in ts format
            #testSuiteGuid      is generated with the same format as testCase
        tstemplate = copy.deepcopy(self.tsxml)
        tssrcp = tstemplate.format(self.sessionID,self.generate_KID(self.GUID))
        #in tc format
            #guid               must be the same with corresponding to testcase in TestCases folder
            #name               prefix ="Test Cases/" + corresponding name of the testcase
        tclinks = []
        for i in range(len(self.generatedTCGUID)):
            tctemplate = copy.deepcopy(self.tstclink)
            tclink = tctemplate.format(self.generatedTCGUID[i],self.groovyScrpName[i])
            tclinks.append(tclink)

        lines = tssrcp.split("\n")
        endTag = lines[-1]
        lines.pop()
        for l in tclinks:
            mini = l.split("\n")
            lines += mini
        lines += [endTag]
        tsscrp = "\n".join(lines)
        try:
            with open(path + self.sessionID+".ts","w") as f:
                f.write(tsscrp)
        except:
            print("File",path + self.sessionID+".ts","could not be opened")

    def removeTestSuites(self):
        log = ""
        path = config.KATALON_DIR + "Test Suites/"
        try:
            os.remove(path + self.sessionID + ".groovy")
            log += f'Removed {path + self.sessionID + ".groovy"}\n'
        except:
            print("File", path + self.sessionID + ".groovy", "not exists")
        
        try:
            os.remove(path + self.sessionID+".ts")
            log += f'Removed {path + self.sessionID+".ts"}\n'
        except:
            print("File",path + self.sessionID+".ts","not exists")

        self.groovyScrpName.clear()
        self.generatedTCGUID.clear()
        return log

        

    def init_data(self):
        self.GUID = '[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}'
        self.tcsample = """<?xml version="1.0" encoding="UTF-8"?>
<TestCaseEntity>
   <description></description>
   <name>{0}</name>
   <tag></tag>
   <comment></comment>
   <testCaseGuid>{1}</testCaseGuid>
</TestCaseEntity>"""

        self.tsxml= """<?xml version="1.0" encoding="UTF-8"?>
<TestSuiteEntity>
   <description></description>
   <name>{0}</name>
   <tag></tag>
   <isRerun>false</isRerun>
   <mailRecipient></mailRecipient>
   <numberOfRerun>0</numberOfRerun>
   <pageLoadTimeout>30</pageLoadTimeout>
   <pageLoadTimeoutDefault>true</pageLoadTimeoutDefault>
   <rerunFailedTestCasesOnly>false</rerunFailedTestCasesOnly>
   <rerunImmediately>false</rerunImmediately>
   <testSuiteGuid>{1}</testSuiteGuid>
</TestSuiteEntity>"""

        self.tstclink="""   <testCaseLink>
        <guid>{0}</guid>
        <isReuseDriver>false</isReuseDriver>
        <isRun>true</isRun>
        <testCaseId>Test Cases/{1}</testCaseId>
    </testCaseLink>"""

        self.tsgroovy = """import static com.kms.katalon.core.checkpoint.CheckpointFactory.findCheckpoint
import static com.kms.katalon.core.testcase.TestCaseFactory.findTestCase
import static com.kms.katalon.core.testdata.TestDataFactory.findTestData
import static com.kms.katalon.core.testobject.ObjectRepository.findTestObject

import com.kms.katalon.core.checkpoint.Checkpoint as Checkpoint
import com.kms.katalon.core.checkpoint.CheckpointFactory as CheckpointFactory
import com.kms.katalon.core.model.FailureHandling as FailureHandling
import com.kms.katalon.core.testcase.TestCase as TestCase
import com.kms.katalon.core.testcase.TestCaseFactory as TestCaseFactory
import com.kms.katalon.core.testdata.TestData as TestData
import com.kms.katalon.core.testdata.TestDataFactory as TestDataFactory
import com.kms.katalon.core.testobject.ObjectRepository as ObjectRepository
import com.kms.katalon.core.testobject.TestObject as TestObject

import com.kms.katalon.core.webservice.keyword.WSBuiltInKeywords as WS
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.kms.katalon.core.mobile.keyword.MobileBuiltInKeywords as Mobile

import internal.GlobalVariable as GlobalVariable

import com.kms.katalon.core.annotation.SetUp
import com.kms.katalon.core.annotation.SetupTestCase
import com.kms.katalon.core.annotation.TearDown
import com.kms.katalon.core.annotation.TearDownTestCase

/**
 * Some methods below are samples for using SetUp/TearDown in a test suite.
 */

/**
 * Setup test suite environment.
 */
@SetUp(skipped = true) // Please change skipped to be false to activate this method.
def setUp() {
	// Put your code here.
}

/**
 * Clean test suites environment.
 */
@TearDown(skipped = true) // Please change skipped to be false to activate this method.
def tearDown() {
	// Put your code here.
}

/**
 * Run before each test case starts.
 */
@SetupTestCase(skipped = true) // Please change skipped to be false to activate this method.
def setupTestCase() {
	// Put your code here.
}

/**
 * Run after each test case ends.
 */
@TearDownTestCase(skipped = true) // Please change skipped to be false to activate this method.
def tearDownTestCase() {
	// Put your code here.
}

/**
 * References:
 * Groovy tutorial page: http://docs.groovy-lang.org/next/html/documentation/
 */"""