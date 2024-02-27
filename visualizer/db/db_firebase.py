#  Created by nphau on 10/29/22, 1:16 PM
#  Copyright (c) 2022 . All rights reserved.
#  Last modified 10/29/22, 1:16 PM
import os
import sys
import time

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)
import firebase_admin
from firebase_admin import credentials, firestore

COLLECTION_PROJECTS = "Projects"
SERVICE_ACCOUNT_KEY = "./db/serviceAccountKey.json"


def timestamp():
    return int(time.time())


class DbFirebase:
    """This is a firebase wrapper class"""

    def __init__(self):
        cred = credentials.Certificate(SERVICE_ACCOUNT_KEY)
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def create_project(self, url, name, type, description):
        self.db.collection(COLLECTION_PROJECTS).add(
            {
                "url": url,
                "name": name,
                "type": type,
                "createdAt": timestamp(),
                "description": description,
                "status": "new",
                "transition": 0,
                "object": 0,
                "place": 0,
                "paths": 0,
                "root": 0,
            }
        )

    def get_projects(self):
        projects = self.db.collection(COLLECTION_PROJECTS) \
            .order_by(field_path='createdAt', direction='DESCENDING').get()
        items = []
        for project in projects:
            item = {}
            for k, v in project.to_dict().items():
                item[k] = v
                item['id'] = project.id
            items.append(item)
        return items

    def delete_project(self, project_id):
        self.db.collection(COLLECTION_PROJECTS).document(project_id).delete()

    def start_project(self, project_id):
        projects_ref = self.db.collection(COLLECTION_PROJECTS).document(project_id)
        projects_ref.update({
            u'startTime': timestamp(),
            u'endTime': timestamp(),
            u'status': "inprogress"
        })

    def end_project(self, project_id, status):
        projects_ref = self.db.collection(COLLECTION_PROJECTS).document(project_id)
        projects_ref.update({
            u'endTime': timestamp(),
            u'status': status
        })

    def project_types(self):
        return [
            {"label": "Web", "value": 1, "disabled": True},
            # {"label": "App", "value": 2, "disabled": True},
        ]


if __name__ == "__main__":
    db = DbFirebase()
    docs = db.get_projects()
    print(docs)
