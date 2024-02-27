import config

from typing import List
import subprocess
import os
import time

class ExecutionEnvironment:
    def __init__(self, appName: str, ) -> None:
        self.supportedApp = ['Moodle', 'Elementary web']
        assert appName in self.supportedApp, f'Unsupported app found {appName}'
        self.appName = appName

    def __call__(self, scripts: List[str]) -> None:
        testNumber = self.writeTestScript(scripts)
        testSuiteName = self.createTestSuite(testNumber)
        self.startApp()
        self.executeTest(testSuiteName)

    def writeTestScript(self, scripts):
        if not os.path.isdir(f'{config.TEST_PROJECT}\\Test Cases\\Generated'):
            os.makedirs(f'{config.TEST_PROJECT}\\Test Cases\\Generated')

        # TODO: Specific for window cmd
        print(f'cd {config.TEST_PROJECT}\\Test Cases\\Generated && del *.tc')
        # subprocess.Popen(f'cd {config.TEST_PROJECT}\\Test Cases\\Generated && rm *.tc')

        for i, script in enumerate(scripts):
            with open(f'{config.TEST_PROJECT}\\Test Cases\\Generated\\Test {i}.tc', 'w+') as file:
                file.write(config.template.format(f'Test {i}', self.generateGUID()))
            if not os.path.isdir(f'{config.TEST_PROJECT}\\Scripts\\Generated\\Test {i}'):
                os.makedirs(f'{config.TEST_PROJECT}\\Scripts\\Generated\\Test {i}')
            with open(f'{config.TEST_PROJECT}\\Scripts\\Generated\\Test {i}\\Script123123123.groovy', 'w+') as file:
                file.write(script)
        return len(scripts)
    
    def generateGUID(self)-> str:
        return 'e836e27b-f387-43b7-8b40-a7659d6f1b1c'

    def startApp(self):
        if self.appName == 'Moodle':
            subprocess.Popen(config.MOODLE_PATH + '..\\Start Moodle.exe')
            time.sleep(10)
            # TODO: Add script to check for app ready
            print('Application started')
        elif self.appName == 'Elementary web':
            subprocess.Popen(f'cd {config.ELEMENTARY_DIR} && yarn start')
            time.sleep(30)
            # TODO: Add script to check for app ready
            print('Application started')


    def executeTest(self, testSuite: str, retry=0):
        '''
            Execute the test with test suite name as input
        '''
        test = subprocess.Popen([
            config.KRE_DIR + '\\katalonc.exe', 
            '-noSplash', 
            '-runMode=console',
            f'-projectPath={config.TEST_PROJECT}'
            '-retry=0', 
            f'-testSuitePath="Test Suites\\{testSuite}"',
            '-browserType="Chrome (headless)"'
        ])

env = ExecutionEnvironment('Moodle')
script = [
    '''
        This is the first script
    ''', 
    '''
        This is the second script
        And many more
    ''']
env.writeTestScript(script)