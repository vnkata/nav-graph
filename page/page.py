from collections import namedtuple
from dataclasses import dataclass
import datetime
import json
import os
import time
from loguru import logger
from element.Element import ActionableElement, ElementFactory
from utils import standardize_value
elfactory = ElementFactory()

@dataclass
class PageData:
    url :str
    title: str 
    screenshot: str = None
    actionable_elements: list[ActionableElement] = None
    candidate_masks: list = None
    page_source: str = None
    access_time: str = datetime.datetime.now().strftime("%b %d, %Y, %H:%M:%S")
    visited_objects = []
    object_uuids = []
    
    @property
    def num_objects(self):
        return 0 if self.actionable_elements is None else len(self.actionable_elements)
    
    def __getstate__(self):
        # object_uuids = None
        # actionable_elements = None
        # logger.debug(f"self.candidate_masks={self.candidate_masks}, type.self.actionable_elements={type(self.actionable_elements[0])}")
        if self.candidate_masks != None:
            object_uuids = {e: m for e, m in zip(self.object_uuids, self.candidate_masks)}
            actionable_elements = [e.json | {'explored': m} for e, m in zip(self.actionable_elements, self.candidate_masks)] 
        else:
            object_uuids = self.object_uuids
            actionable_elements = [e.json for e in self.actionable_elements]

        odict = {
                    'title': self.title,
                    'url': self.url,
                    'screenshot': self.screenshot,
                    'access_time': self.access_time,
                    'object_uuids': object_uuids,
                    'num_objects': self.num_objects,
                    'actionable_elements': actionable_elements                
                }
        return odict
    
    # @property
    # def set_age(self, x):
    # def update_object_uuids(self, uuids:list):
    #     if self.candidate_masks != None:
    #         self.object_uuids = {e: m for e, m in zip(uuids, self.candidate_masks)}
    #     else:
    #         self.object_uuids = {e: False for e in uuids}
    
    # def update_actionable_elements(self, candidate_masks:list):
    #     self.candidate_masks = candidate_masks
    #     if self.candidate_masks != None:
    #         self.actionable_elements = [e.json | {'explored': m} for e, m in zip(actionable_elements, self.candidate_masks)] 
    #     else:
    #         self.actionable_elements = [e.json | {'explored': False} for e in actionable_elements] 

    def __setstate__(self, dict):
        print ("setstate, ", dict.keys())
        self.title = dict.get('title', None)
        self.url = dict.get('url', None)
        self.screenshot = dict.get('screenshot', None)
        self.object_uuids = dict.get('object_uuids', [])
        self.actionable_elements =  [elfactory.get(e) for e in  dict.get('actionable_elements', [])]
        # self.num_objects = dict.get('num_objects', 0)


    def export(self, filename):
        with open(filename, "w") as fp:
            json.dump(self.__getstate__(), fp, indent=4, sort_keys=True)

        # TODO: workaround solution, need to pass `PageID` in __init__ or elsewhere.
        page_id = os.path.basename(os.path.dirname(filename))
        new_log_f = os.path.join(os.path.dirname(os.path.dirname(filename)), f"{page_id}_{int(time.time())}_{standardize_value(self.title)}.info")
        with open(new_log_f, "w") as fp:
            json.dump(self.__getstate__(), fp, indent=4, sort_keys=True)
