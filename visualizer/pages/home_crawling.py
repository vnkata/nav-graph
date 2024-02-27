#  Created by nphau on 11/20/22, 4:41 PM
#  Copyright (c) 2022 . All rights reserved.
#  Last modified 11/20/22, 4:41 PM
import crawler
import os
import crawler_logger
import multiprocessing
import os
import sys
import shutil

multiprocessing.set_start_method('fork')

global server_process


def create_log_file(project_id):
    folder = crawler_logger.get_log_folder(project_id)
    if os.path.exists(folder):
        try:
            shutil.rmtree(folder)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))
    os.mkdir(folder)
    file = f"./{crawler_logger.get_log_file_path(project_id)}"
    open(file, "w")


def start_crawling(selected_project):
    project_id = selected_project['id']
    url = selected_project['url']
    create_log_file(project_id)

    def run():
        crawler.start(url, project_id)

    global server_process
    server_process = multiprocessing.Process(target=run)
    server_process.start()


def stop_crawling():
    try:
        server_process.terminate()
    except Exception as e:
        print(e)
