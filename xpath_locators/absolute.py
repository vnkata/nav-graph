from utils import get_position
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

def get_absolute_xpath(ele: WebElement, driver) -> str:
    """Get XPath value of an (Selenium) WebElement

    Args:
        ele (WebElement): The WebElement object 

    Returns:
        str: XPath of WebElement [el]
    """
    xpath = ""
    components = []
    
    current_ele = ele
    # while (current_ele.tag_name != 'html'):
    #     comp = {
    #         "tag_name": current_ele.tag_name,
    #         "position": get_position(current_ele)
    #     }
    #     components.append(comp)
    #     current_ele = current_ele.find_element(by=By.XPATH, value="..")
    #
    # for i in range(len(components) - 1, -1, -1):
    #     comp = components[i]
    #     xpath += f"/{comp['tag_name']}"
    #     if comp["position"] is not None:
    #         xpath += f"[{comp['position']}]"

    ancestors = current_ele.find_elements(By.XPATH, ".//ancestor::*")
    xpath_expr = ""
    for ancestor in ancestors:
        position = get_position(ancestor)
        if position is not None:
            xpath_expr += "/{}[{}]".format(ancestor.tag_name.lower(), position)
    xpath_expr += "/{}[{}]".format(current_ele.tag_name.lower(), get_position(current_ele))
    
    return '/html' + xpath

    #
    # xpath_expr = ""
    # for ancestor in ancestors:
    #     position = get_position(ancestor)
    #     if position is not None:
    #         xpath_expr += "/{}[{}]".format(ancestor.tag_name.lower(), position)
    # xpath_expr += "/{}[{}]".format(current_ele.tag_name.lower(), get_position(current_ele))