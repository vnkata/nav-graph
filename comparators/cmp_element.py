from abc import abstractmethod
from typing import List
from element.Element import ActionableElement, ElementFactory

class ElementComparator(object):
    def __init__(self):
        pass
    
    @abstractmethod
    def is_contain(self, obj, SUBSET_REP_OBJ) -> str:
        pass

class BasicElementComparator(ElementComparator):
    def __init__(self):
        super().__init__()

    def is_contain(self, obj, SUBSET_REP_OBJ)-> str:
        for obj_id, stored_obj in SUBSET_REP_OBJ.items():
            if obj == stored_obj:
                return obj_id
        else:
            return None

class XpathBasedElementComparator(ElementComparator):
    def __init__(self):
        super().__init__()

    def is_contain(self, obj: ActionableElement, SUBSET_REP_OBJ: dict[str,ActionableElement])-> str:
        for obj_id, stored_obj in SUBSET_REP_OBJ.items():
            try:
                if obj == stored_obj and obj.get_attribute('absolute_xpath') == stored_obj.get_attribute('absolute_xpath') :
                    return obj_id
            except:
                if obj.get_attribute('absolute_xpath') == stored_obj.get_attribute('absolute_xpath') :
                    return obj_id
        else:
            return None

def less_strict_element_list_comparator(a_elements: List[ActionableElement], b_elements: List[ActionableElement]) -> bool:
    assert None not in a_elements
    assert None not in b_elements

    union = []
    intersection =  []#set(a_elements).intersection(b_elements)
    for ac in a_elements:
        if ac in b_elements:
            intersection.append(ac)

    for ac in a_elements:
        if ac not in union: union.append(ac)
    for bc in b_elements:
        if bc not in union: union.append(bc)

    if ((len(intersection) * 1.0) /  len(union) ) > 0.85:
        return True
    else:
        return False