import string
import random
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By


def all_preceding_siblings(ele: WebElement):
    preceding_sibling_path = f"./preceding-sibling::*"
    try:
        siblings = ele.find_elements(By.XPATH, preceding_sibling_path)
        return siblings
    except:
        return []


def all_following_siblings(ele: WebElement):
    following_sibling_path = f"./following-sibling::*"
    try:
        siblings = ele.find_elements(By.XPATH, following_sibling_path)
        return siblings
    except:
        return []


def preceding_siblings(ele: WebElement):
    preceding_sibling_path = f"./preceding-sibling::{ele.tag_name}"
    try:
        siblings = ele.find_elements(By.XPATH, preceding_sibling_path)
        return siblings
    except:
        return []


def following_siblings(ele: WebElement):
    following_sibling_path = f"./following-sibling::{ele.tag_name}"
    try:
        siblings = ele.find_elements(By.XPATH, following_sibling_path)
        return siblings
    except:
        return []


def get_position(ele: WebElement, tryAll=False):
    """
    Get the position of the web element with respect to its preceding siblings.
    In other words, if the element is in a list, return the index of the list element.

    Parameters
    ----------
    ele : WebElement
        The WebElement object
    tryAll : bool
        A flag to toggle whether the position of the element is relative to siblings of same tag name or all siblings
    """
    position = 1
    if tryAll:
        position += len(preceding_siblings(ele))
        if position == 1 and len(following_siblings(ele)) == 0:
            position = None
    else:
        position += len(all_preceding_siblings(ele))
        if position == 1 and len(all_following_siblings(ele)) == 0:
            position = None
    return position


def randomword(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def randomid(fixed_digits=6):
    return str(random.randrange(111111, 999999, fixed_digits))

# special_characters = [",", ".", "|", "-", ":", "!", "", "/"]
# def fname(str):
#     for c in special_characters: str = str.replace(c, "")
#     return str

def standardize_value(data):
    __special_characters = [",", ".", "|", "-", ":", "!", "", "/", "-", " ", "_", "?", "&"]
    for c in __special_characters: data = data.replace(c, "")
    return data
