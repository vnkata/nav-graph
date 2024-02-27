import os
from shutil import copy
from fnmatch import fnmatch

# root = 'Everleagues/'
# pattern = "*.groovy"

# for path, subdirs, files in os.walk(root):
#     for name in files:
#         if fnmatch(name, pattern):
#             copy(os.path.join(path, name), 'InputEverleagues')

import glob
# absolute katalon project path
#pattern = 'C:/Users/Prometheus/Downloads/elementary-main-17/Katalon_pj/Working/**/*.groovy'
pattern = 'C:/Users/Prometheus/Downloads/moodle-main-14/Working/**/*.groovy'
#pattern = 'C:/Users/Prometheus/Downloads/moodle-main-29/Working/**/*.groovy'
#pattern = 'C:/Users/Prometheus/Downloads/moodle-main-7/Working/**/*.groovy'

for path in glob.glob(pattern, recursive=True):
    copy(path, 'GroovyParser/Data')

#element-17 test number
"""1, 2, 3, 4, 6, 20, 23, 24, 25, 28, 29, 30, 31,
 33, 34, 35, 37, 38, 40, 41, 43, 44, 45, 
49, 51, 54, 55, 56, 58, 59, 62, 63, 65, 67, 71, 73, 76, 77, 
78, 79, 80, 81, 82, 84, 85, 87, 89, 90, 91, 93    """

# from plyer import notification
# import time
# print("doing...")
# time.sleep(5)
# notification.notify(title = "Finished!!!", message = "Successful")

