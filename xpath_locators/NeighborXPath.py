from shutil import ExecError
from typing import List, Union
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from .XPath import XPath
from .absolute import get_absolute_xpath


class NeighborXPathGenerator(object):
    def __init__(self, element: WebElement, driver: WebDriver) -> None:
        self.__element = element
        self.__driver = driver
        self.__xpaths: List[XPath] = None
        self.__unpreferredTags = [
            "main", "style", "title", "body", "iframe", "path",
            "script", "ul", "link", "svg", "nav", "noscript",
            "meta", "option", "p", "br", "head", "header", "footer"
        ]
            
    def getNeighborXPath(self, neighborElmt: WebElement, axis: str) -> XPath:
        """
        Create an XPath for the current target element based on the neighbor element of the target.
        For example, if the neighbor is preceding the target, then the XPath will move forward ('following' axis) from the neighbor element to get the target element

        Parameters
        ----------
        neighborElmt : WebElement
            The element preceding or following the target element, no matter the distance
        axis : str
            Determine the direction to move from the neighbor. Value can be "preceding" or "following"
        """
        try:
            text = neighborElmt.get_attribute("textContent")
            normalizedText = ' '.join(str(text).split()) if text is not None else ""
            if normalizedText == "" or normalizedText.find("\"") != -1:
                return None
            xpath = f"(.//*[normalize-space(text()) or normalize-space(.) = \"{normalizedText}\"])"
            elements = self.__driver.find_elements(By.XPATH, xpath)
            position = elements.index(neighborElmt) + 1
            xpath += f"[{position}]/{axis}::{self.__element.tag_name}"
            elements = self.__driver.find_elements(By.XPATH, xpath)
            if axis == "preceding":
                elements.reverse()
            position = elements.index(self.__element) + 1
            xpath += f"[{position}]"
            return XPath(xpath)
        except ValueError as valErr:
            return None
    
    @staticmethod
    def findNextNeighbor(currentEle: WebElement, axis: str) -> Union[WebElement, None]:
        if axis not in ["preceding", "following"]:
            raise Exception("The axis of neighbor elements can only be 'preceding' or 'following'")
        try:
            neighborEle = currentEle.find_element(By.XPATH, f"{axis}::*[1]")
            return neighborEle
        except:
            return None
    
    def generate_neighbor_xpaths(self, n: int):
        """
        Generate a list of neighbor xpaths for the current target web element.

        Parameters
        ----------
        n : int
            The number of neighbor elements on each direction to extract the neighbor xpaths
        """
        if self.__xpaths is None:
            self.__xpaths = []
        else:
            return self.__xpaths
        # Generate neighbor xpaths based on preceding elements
        i = 0
        neighborEle = NeighborXPathGenerator.findNextNeighbor(self.__element, "preceding")
        axis = "following"
        while i < n and neighborEle is not None:
            if neighborEle.tag_name not in self.__unpreferredTags:
                xpath = self.getNeighborXPath(neighborEle, axis)
                if xpath is not None:
                    self.__xpaths.append(xpath)
                    i += 1
            neighborEle = NeighborXPathGenerator.findNextNeighbor(neighborEle, "preceding")
        
        # Generate neighbor xpaths based on following elements
        i = 0
        neighborEle = NeighborXPathGenerator.findNextNeighbor(self.__element, "following")
        axis = "preceding"
        while i < n and neighborEle is not None:
            if neighborEle.tag_name not in self.__unpreferredTags:
                xpath = self.getNeighborXPath(neighborEle, axis)
                if xpath is not None:
                    self.__xpaths.append(xpath)
                    i += 1
            neighborEle = NeighborXPathGenerator.findNextNeighbor(neighborEle, "following")
        return self.__xpaths

def get_neighbor_xpath(element, driver) -> str:
    nbxGen = NeighborXPathGenerator(element, driver)
    return str(nbxGen.generate_neighbor_xpaths(1)[0])