from os import getcwd


TEST_DIR = "GroovyParser/Output"
INPUT_DIR = "GroovyParser/Data"
OUTPUT_RAW_DIR = 'Output/'
OUTPUT_DIR = 'OutputGroovy/'
#KATALON_DIR = 'C:/Users/Prometheus/Downloads/elementary-main-17/Katalon_pj/Bonus_SE/'
KATALON_DIR = 'C:/Users/Prometheus/Downloads/moodle-main-14/Test Automation - SE Bonus/'
#KATALON_DIR = 'C:/Users/Prometheus/Downloads/moodle-main-29/Test-Automation-SE-Bonus/'
#KATALON_DIR = 'C:/Users/Prometheus/Downloads/moodle-main-7/Katalon-Moodle-7/'
K_PROJECT_NAME = 'Test Automation - SE Bonus.prj'
ABS_DIR = getcwd() + "/test_generator/"
LOG_DIR = ABS_DIR + "Log/"
FTEST_DIR = ABS_DIR + "Tests/"
KRE_DIR = 'C:/Users/Prometheus/Downloads/Katalon_Studio_Engine_Windows_64-8.2.5/'
API_KEY = """-apiKey=e8f6fba0-5a1f-4663-b08c-10cc19c615e4"""

#element-17: 
# ./katalonc -noSplash  -runMode=console -projectPath="C:\Users\Prometheus\Downloads\elementary-main-17\Katalon_pj\Bonus_SE\Bonus_SE.prj" -retry=0 -testSuitePath="Test Suites/Run all test case" -browserType="Chrome" -apiKey=e8f6fba0-5a1f-4663-b08c-10cc19c615e4 --config -webui.autoUpdateDrivers=true
#moodle-14: 
# ./katalonc -noSplash  -runMode=console -projectPath="C:\Users\Prometheus\Downloads\moodle-main-14\Test Automation - SE Bonus\Test Automation - SE Bonus.prj" -retry=0 -testSuitePath="Test Suites/Run_All_Test_Cases" -browserType="Chrome" -apiKey=e8f6fba0-5a1f-4663-b08c-10cc19c615e4 --config -webui.autoUpdateDrivers=true
#moodle-7: 
# ./katalonc -noSplash  -runMode=console -projectPath="C:\Users\Prometheus\Downloads\moodle-main-7\Katalon-Moodle-7\Test Automation - SE Bonus.prj" -retry=0 -testSuitePath="Test Suites/Run all test cases" -browserType="Chrome" -apiKey=e8f6fba0-5a1f-4663-b08c-10cc19c615e4 --config -webui.autoUpdateDrivers=true
#moodle-29: 
# ./katalonc -noSplash  -runMode=console -projectPath="C:\Users\Prometheus\Downloads\moodle-main-29\Test-Automation-SE-Bonus\Test-Automation-SE-Bonus.prj" -retry=0 -testSuitePath="Test Suites/Run all test cases" -browserType="Chrome" -apiKey=e8f6fba0-5a1f-4663-b08c-10cc19c615e4 --config -webui.autoUpdateDrivers=true