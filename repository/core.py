from pathlib import Path

from numpy import uint
from element.Element import ActionableElement, RuntimeActionableElement
from comparators.cmp_element import BasicElementComparator, XpathBasedElementComparator
from utils import randomword

import glob
import json
import uuid as uuid_m
from typing import Union
from element.Element import ElementFactory
from loguru import logger
from collections import defaultdict


# TODO: Will fix later
available_tags = ['a', 'button', 'input', 'form', 'select']

class ObjectManager(object):
    def __init__(self, repository_directory:str='./running_logs', working_dir: str='/tmp', load_exist_objs = True):
        self.working_dir = working_dir
        Path(working_dir + "/objects").mkdir(parents=True, exist_ok=True)
        Path(working_dir + "/objects/all").mkdir(parents=True, exist_ok=True)
        Path(working_dir + "/objects/visited").mkdir(parents=True, exist_ok=True)

        self.object_repo: defaultdict[str, dict[str, ActionableElement]]= defaultdict(dict)
        self.visited_objects: dict[str, ActionableElement] = {}
        if load_exist_objs: self.load_objects(repository_directory)
            
    def load_objects(self, repository_directory:str) -> None:
        ef = ElementFactory()
        for each_obj in glob.glob(repository_directory + '/**/objects/all/*.json', recursive=True):
            old_obj_dir = each_obj.replace('\\',"/")
            with open(old_obj_dir) as f:
                data = json.load(f)
            assert len(data.keys()) > 0
            self.object_repo[data['tag_name']][data['uuid']]=ef.from_dict(data)
            
        num_loaded_objs = 0
        for tag in available_tags: num_loaded_objs += len(self.object_repo[tag].keys())
        print("#loaded objects (in repository): ",num_loaded_objs)
            
        for each_obj in glob.glob(repository_directory + '/**/objects/visited/*.json', recursive=True):
            old_visited_obj_dir = each_obj.replace('\\',"/")
            with open(old_visited_obj_dir) as f:
                data = json.load(f)
            assert len(data.keys()) > 0
            element = ef.from_dict(data)
            self.visited_objects[element.get_attribute('uuid')] = element
            
        print("#visited_objects: ",len(self.visited_objects))
                
    def push_object(self, el: Union[ActionableElement, RuntimeActionableElement], 
                        e_comparator = XpathBasedElementComparator(), 
                        save_to_disk=True) -> ActionableElement:

        serialized_object: ActionableElement= None
        if isinstance(el, RuntimeActionableElement):
            _current_element = el.to_actionable_element()
        elif isinstance(el, ActionableElement):
            _current_element = el 
        object_id = e_comparator.is_contain(_current_element, self.object_repo[_current_element.get_attribute('tag_name')])
        if object_id is None:
            object_id = str(uuid_m.uuid4())
            _current_element.assign_uuid(object_id)

            self.object_repo[_current_element.get_attribute('tag_name')][object_id] = _current_element
            if save_to_disk:
                with open(f'{self.working_dir}/objects/all/obj.{object_id}.json', 'w') as f:
                        json.dump(_current_element.json, f, indent=4, sort_keys=True)
        else:
            _current_element.assign_uuid(object_id)
        serialized_object = _current_element

        return serialized_object

    def push_objects(self, actionable_elements: list[Union[ActionableElement, RuntimeActionableElement]], 
                        e_comparator = XpathBasedElementComparator(), 
                        save_to_disk=True) -> list[ActionableElement]:

        added_masks = [False] * len(actionable_elements)
        serialized_objects: list[ActionableElement]= []
        for idx, el in enumerate(actionable_elements): 
            if isinstance(el, RuntimeActionableElement):
                _current_element = el.to_actionable_element()
            elif isinstance(el, ActionableElement):
                _current_element = el 

            object_id = e_comparator.is_contain(_current_element, self.object_repo[_current_element.get_attribute('tag_name')])
            if object_id is None:
                added_masks[idx] = True
                object_id = str(uuid_m.uuid4())
                _current_element.assign_uuid(object_id)

                self.object_repo[_current_element.get_attribute('tag_name')][object_id] = _current_element
                if save_to_disk:
                    with open(f'{self.working_dir}/objects/all/obj.{object_id}.json', 'w') as f:
                            json.dump(_current_element.json, f, indent=4, sort_keys=True)
            else:
                _current_element.assign_uuid(object_id)
            serialized_objects.append(_current_element)

        return serialized_objects, added_masks
                    
    def add_visited_object(self, actionable_el: ActionableElement):
        element_uuid =  actionable_el.get_attribute('uuid')
        self.visited_objects[element_uuid] = actionable_el
        with open(f'{self.working_dir}/objects/visited/obj.{element_uuid}.json', 'w') as f:
                        json.dump(actionable_el.json, f, indent=4, sort_keys=True)
    
    def generate_mask(self, actionable_els: list[ActionableElement]):
        candidate_masks = [False] * len(actionable_els)
        visited_elements = self.visited_objects.values()
        for idx,curr_el in enumerate(actionable_els):
            candidate_masks[idx] =  not (curr_el in visited_elements )
        return candidate_masks
    
    def get_object(self, uuid) -> Union[ActionableElement, None]:
        if uuid in self.visited_objects:
            return self.visited_objects[uuid]

        for tag in available_tags:
            if uuid in self.object_repo[tag].keys():
                output =  self.object_repo[tag][uuid]
                if isinstance(output, RuntimeActionableElement):
                    output = output.to_actionable_element()
                assert isinstance(output, ActionableElement) == True
                return output
        logger.error(f"Can not found element with uuid={uuid}")
        return None
    
    @property
    def unexplored_objects(self) -> list[str]:
        all_objects = []
        for tag in available_tags:
            for uuid in self.object_repo[tag].keys():
                if uuid not in self.visited_objects:
                    all_objects.append(uuid)
        return all_objects
    
    def num_objects(self):
        num_objects = 0
        for tag in available_tags: num_objects += len(self.object_repo[tag].keys())
        return num_objects    
    def get_by_tagname(self,tag_name):
        return self.object_repo[tag_name]