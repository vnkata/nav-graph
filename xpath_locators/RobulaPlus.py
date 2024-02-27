from typing import List, Union
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from io import StringIO
from .XPath import XPath
from utils import get_position

def cmp_to_key(cmp_function):
    """Transfer cmp=func to key=func"""

    class K(object):
        def __init__(self, obj, *args):
            self.obj = obj

        def __lt__(self, other):
            return cmp_function(self.obj, other.obj) < 0

        def __gt__(self, other):
            return cmp_function(self.obj, other.obj) > 0

        def __eq__(self, other):
            return cmp_function(self.obj, other.obj) == 0

        def __le__(self, other):
            return cmp_function(self.obj, other.obj) <= 0

        def __ge__(self, other):
            return cmp_function(self.obj, other.obj) >= 0

        def __ne__(self, other):
            return cmp_function(self.obj, other.obj) != 0

    return K


class RobulaPlusOptions(object):
    """
    :attribute - attributePriorizationList: A prioritized list of HTML attributes,
                which are considered in the given order.
    :attribute - attributeBlackList: Contains HTML attributes,
                 which are classified as too fragile and are ignored by the algorithm.
    """

    def __init__(self):
        self.attributePriorizationList = ['name', 'class', 'title', 'alt', 'value']
        self.attributeBlackList = ['href','src','onclick','onload','tabindex','width','height','style','size','maxlength','data-io-article-url', 'action']


class RobulaPlus(object):
    def __init__(self, element: WebElement, driver: WebDriver, options: RobulaPlusOptions = None):
        self.__element = element
        self.__driver = driver
        if options is None:
            options = RobulaPlusOptions()
        self.__attributePriorizationList = options.attributePriorizationList
        self.__attributeBlackList = options.attributeBlackList
        self.__ancestors = None
        self.XPathList = []
    
    def updateElementDriver(self, element, driver):
        self.__element = element
        self.__driver = driver

    def canPrioritizeAttr(self, name: str, value) -> bool:
        if "id" in name or "name" in name or "class" in name or "title" in name:
            self.__attributePriorizationList.append(name)
            return True
        return False

    def canBlacklistAttr(self, name: str, value) -> bool:
        name = name.lower()
        value = str(value).lower()
        if "/" in value or "\"" in value:
            self.__attributeBlackList.append(name)
            return True
        if name.startswith(("on")):
            self.__attributeBlackList.append(name)
            return True
        if any([substring in name for substring in ["width", "height", "size", "length"]]):
            self.__attributeBlackList.append(name)
            return True
        if any([substring in value for substring in ["{", "}", ".", "(", ")", "click"]]):
            self.__attributeBlackList.append(name)
            return True
        return False

    def uniquelyLocate(self, xPath: str) -> bool:
        elements = self.__driver.find_elements(By.XPATH, xPath)
        return len(elements) == 1 and elements[0] == self.__element

    def getAncestors(self, distance: int = None) -> Union[WebElement, List[WebElement], None]:
        if self.__ancestors is None:
            self.__ancestors = self.__element.find_elements(By.XPATH, "ancestor-or-self::*")
        if distance is None:
            return self.__ancestors
        return self.__ancestors[-1 - distance]

    def transfConvertStar(self, xPath: XPath) -> list:
        output = []
        if xPath.startsWith('//*'):
            ancestor = self.getAncestors(xPath.getLength() - 1)
            newXP = XPath('//' + ancestor.tag_name.lower() + xPath.substring(3))
            if xPath.headHasPositionPredicate():
                newXP.replaceHeadPosition(get_position(ancestor))
            output.append(newXP)
        return output

    def transfAddId(self, xPath: XPath) -> list:
        output = []
        ancestor = self.getAncestors(xPath.getLength() - 1)
        _id = ancestor.get_attribute("id")
        if _id and not xPath.headHasAnyPredicates():
            newXPath = XPath(str(xPath))
            newXPath.addPredicateToHead(f'[@id="{_id}"]')
            output.append(newXPath)
        return output

    def transfAddText(self, xPath: XPath) -> list:
        output = []
        ancestor: WebElement = self.getAncestors(xPath.getLength() - 1)
        if not xPath.headHasTextPredicate() and not xPath.headHasPositionPredicate() and ancestor.text and str(ancestor.text).find("\"") == -1 and str(ancestor.text).find("/") == -1:
            newXPath = XPath(str(xPath))
            newXPath.addPredicateToHead(f'[contains(text(), "{ancestor.text}")]')
            output.append(newXPath)
        return output

    def transfAddAttribute(self, xPath: XPath) -> list:
        output = []
        if not xPath.headHasAnyPredicates():
            ancestor: WebElement = self.getAncestors(xPath.getLength() - 1)
            attributes = ancestor.get_property("attributes")
            
            # add priority attributes to output
            for attr in attributes:
                if attr["name"] in self.__attributePriorizationList or self.canPrioritizeAttr(attr["name"], attr["value"]):
                    newXPath = XPath(str(xPath))
                    newXPath.addPredicateToHead("[@{}='{}']".format(attr["name"], attr["value"]))
                    output.append(newXPath)
            
            # append all other non-blacklist attributes to output
            for attr in attributes:
                if attr["name"] not in self.__attributeBlackList and attr["name"] not in self.__attributePriorizationList:
                    if self.canBlacklistAttr(attr["name"], attr["value"]):
                        continue
                    newXPath = XPath(str(xPath))
                    newXPath.addPredicateToHead("[@{}='{}']".format(attr["name"], attr["value"]))
                    output.append(newXPath)
        return output

    def transfAddPosition(self, xPath: XPath) -> list:
        output = []
        ancestor = self.getAncestors(xPath.getLength() - 1)
        if not xPath.headHasPositionPredicate():
            newXPath = XPath(str(xPath))
            headTag = newXPath.getHeadTag()
            position = get_position(ancestor, headTag == "*")
            newXPath.addPredicateToHead(f"[{position}]")
            output.append(newXPath)
        return output

    def transfAddLevel(self, xPath: XPath) -> list:
        output = []
        if xPath.getLength() - 1 < len(self.__ancestors):
            output.append(XPath('//*' + xPath.substring(1)))

        return output

    def generatePowerSet(self, a: list) -> list:
        """generate all combinations"""
        if len(a) == 0:
            return [[]]
        cs = []
        for c in self.generatePowerSet(a[1:]):
            cs += [c, c + [a[0]]]
        return cs

    def elementCompareFunction(self, attr1: dict, attr2: dict) -> int:
        for element in self.__attributePriorizationList:
            if element == attr1["name"]:
                return -1

            if element == attr2["name"]:
                return 1

        return 0

    def compareListElementAttributes(self, set1: list, set2: list) -> int:
        if len(set1) < len(set2):
            return -1

        if len(set1) > len(set2):
            return 1

        for i in range(0, len(set1)):
            if set1[i] != set2[i]:
                return self.elementCompareFunction(set1[i], set2[i])

        return 0

    def transfAddAttributeSet(self, xPath: XPath) -> list:
        output = []
        ancestor = self.getAncestors(xPath.getLength() - 1)
        if not xPath.headHasAnyPredicates():
            # add id to attributePriorizationList
            self.__attributePriorizationList.insert(0, 'id')
            attributes = ancestor.get_property("attributes")

            # remove black list attributes
            attributes = [{"name": attr["name"], "value": attr["value"]} for attr in attributes if attr["name"] not in self.__attributeBlackList]

            # generate power set
            attributePowerSet = self.generatePowerSet(attributes)

            # remove sets with cardinality < 2
            attributePowerSet = filter(lambda x: len(x) >= 2, attributePowerSet)

            # sort elements inside each powerset
            for attributeSet in attributePowerSet:
                attributeSet = sorted(attributeSet, key=cmp_to_key(self.elementCompareFunction))

            # sort attributePowerSet
            attributePowerSet = sorted(attributePowerSet, key=cmp_to_key(self.compareListElementAttributes))

            # remove id from attributePriorizationList
            self.__attributePriorizationList.pop(0)

            # convert to predicate
            for attributeSet in attributePowerSet:
                key = attributeSet[0]['name']
                value = attributeSet[0]['value']
                predicate = f"[@{key}='{value}'"

                for i in range(1, len(attributeSet)):
                    key = attributeSet[i]['name']
                    value = attributeSet[i]['value']
                    predicate += f" and @{key}='{value}'"

                predicate += ']'
                newXPath = XPath(str(xPath))
                newXPath.addPredicateToHead(predicate)
                output.append(newXPath)

        return output

    def getRobustXPath(self):
        if len(self.XPathList) > 0:
            return self.XPathList
        self.XPathList = [XPath('//*')]
        while len(self.XPathList) > 0:
            xPath = self.XPathList.pop(0)
            temp = []
            #print("XPath List in this iteration:", *self.XPathList, sep="\n\t")
            temp.extend(self.transfConvertStar(xPath))
            #print("Temp after convert star:", *temp, sep="\n\t")
            temp.extend(self.transfAddId(xPath))
            #temp.extend(self.transfAddText(xPath)) # Adding texts is too fragile
            #print("Temp after add ID:", *temp, sep="\n\t")
            temp.extend(self.transfAddAttribute(xPath))
            #print("Temp after add attribute:", *temp, sep="\n\t")
            temp.extend(self.transfAddAttributeSet(xPath))
            #print("Temp after add attribute set:", *temp, sep="\n\t")
            temp.extend(self.transfAddPosition(xPath))
            #print("Temp after add position:", *temp, sep="\n\t")
            temp.extend(self.transfAddLevel(xPath))
            #print("Temp after add level:", *temp, sep="\n\t")
            temp = sorted(set(temp), key=lambda key: str(key))  # removes duplicates and sort by len
            # for x in temp:
            #     if str(x) == "//*[@action='[@itemprop='itemListElement']/demo/index.php/cart/addItem']/*/*":
            #         print("Error in this iteration!")
            # print()
            for x in temp:
                if self.uniquelyLocate(str(x)):
                    return x
                self.XPathList.append(x)

        return self.XPathList
rgl = None
def get_robula_xpath(element, driver) -> str:
    global rgl
    if rgl is None:
        rbl = RobulaPlus(element, driver)
    else:
        rbl.updateElementDriver(element, driver)
    return str(rbl.getRobustXPath())