from dataclasses import dataclass
from element.operators import find_element
from loguru import logger

class Assertion:
    def __init__ (self, object_uuid, data):
        self.object_uuid: str = object_uuid # e.g: 00457be8-0726-4c8b-b875-d69d7a6f36d3
        self.data: str = data #expected value of `attr` that you want to be asserted (optional)

    def verify(self, driver, objManager):
        pass


class verifyTextPresent(Assertion):
    def __init__ (self, *args, **kwargs):
        super(verifyTextPresent, self).__init__(*args, **kwargs)
    
    def verify(self, driver, objManager):
        if self.data in driver.page_source:
            return True
        else:
            return False
        

class verifyElementVisible(Assertion):
    def __init__ (self, *args, **kwargs):
        super(verifyElementVisible, self).__init__(*args, **kwargs)
        self.data = None
    
    def verify(self, driver, objManager):
        element = objManager.get_object(self.object_uuid)
        e = find_element(element, driver)
        return True if e and e.is_attached() else False


class verifyElementAttributeValue(Assertion):
    def __init__ (self, *args, **kwargs):
        super(verifyElementAttributeValue, self).__init__(*args, **kwargs)

    def verify(self, driver, objManager):
        _attr, _expected_value = self.data.split(";")
        element = objManager.get_object(self.object_uuid)
        e = find_element(element, driver)
        if not e:
            logger.info(f"unable to find element: {self.object_uuid}")
            return False
        
        # a simple hack for attribute `href`
        if _attr == "href":
            if _expected_value in e._runtime_element.get_attribute(_attr): 
                return True
            else:
                return False


        if e._runtime_element.get_attribute(_attr) == _expected_value:
            return True
        else:
            return False 

class verifyElementHasAttribute(Assertion):
    def __init__ (self, *args, **kwargs):
        super(verifyElementHasAttribute, self).__init__(*args, **kwargs)

    def verify(self, driver, objManager):
        _attr = self.data
        element = objManager.get_object(self.object_uuid)
        e = find_element(element, driver)
        if not e:
            logger.info(f"unable to find element: {self.object_uuid}")
            return False
        if e._runtime_element.get_attribute(_attr) !=  None:
            return True
        else:
            return False 


def dict2assertion (dict):
    assert "assertion_type" in dict
    assert "object_uuid" in dict
    assert "data" in dict

    
    all_assertions = {
        "verifyTextPresent":verifyTextPresent,
        "verifyElementVisible": verifyElementVisible,
        "verifyElementAttributeValue": verifyElementAttributeValue,
        "verifyElementHasAttribute": verifyElementHasAttribute,
    }
    return all_assertions.get(dict['assertion_type'])(
        object_uuid=dict["object_uuid"], 
        data = dict["data"])