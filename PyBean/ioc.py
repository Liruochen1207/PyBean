import xml.etree.ElementTree as ET
from typing import Dict, List

from PyBean.bean import Bean, Property
from PyBean.by import *




def boolAttr(inp: str):
    if inp.lower() == 'true' or inp == "1":
        return True
    elif inp.lower() == 'false' or inp == "0":
        return False
    else:
        raise ValueError("Invalid bool input")


def matchBrackets(inp: str):
    state = 0
    front = ""
    end = ""
    if "{" in inp or "}" in inp:
        state += 1
    if "[" in inp or "]" in inp:
        state += 1

    if state > 1:
        raise ValueError("Invalid brackets")
    if "{" in inp:
        front = "{"
        end = "}"
    elif "[" in inp:
        front = "["
        end = "]"
    SPLIT = inp.split(',')
    args = []
    for br in SPLIT:
        tips = 0
        cache = ""
        head = False
        tail = False
        ready = ""
        for s in br:
            cache += s
            if s == front:
                head = True
                continue
            if s == end:
                tail = True
                break
            if head:
                ready += s
        if (not head) and (not tail):
            ready = cache.strip()
        elif (head and tail):
            if front == "{":
                tips = 1
            if front == "[":
                tips = 2
        else:
            tips = -1
        if ready.isdigit():
            ready = float(ready)
        if ready == "true":
            ready = True
        if ready == "false":
            ready = False
        args.append((ready, tips))
    return args


class FuncStringLoader:
    def __init__(self, string: str = ""):
        self.string = string
        self.functionName = ""

    def setString(self, string: str):
        self.string = string

    def load(self):
        print(self.string)
        if self.string:
            return eval(self.string)
        else:
            raise ValueError("No string input")


class ElementLoader:
    def __init__(self, element: ET.Element):
        self.element = element
        self.parent = None
        self.children = []

    def setParent(self, parent):  # parent is a ElementLoader
        self.parent = parent

    def addChild(self, child):  # child is a ElementLoader
        self.children.append(child)


def getAttributeFromElement(element: ET.Element, name: str):
    attribute = element.attrib
    if name in attribute:
        return attribute[name]
    return None





class ApplicationContext:
    def __init__(self, applicationContextPath: str):
        self.tree = ET.parse(applicationContextPath)
        self.root = self.tree.getroot()
        self.pointer: ET.Element = self.root
        self.depth = -1
        self.__scanDiction: Dict[int, List[ElementLoader]] = self.__scan()

    def pointerLength(self) -> int:
        return self.pointer.__len__()

    def pointerHasChildren(self) -> bool:
        return self.pointerLength() > 0

    def getPointerChildren(self) -> List[ET.Element]:
        li = []
        for index in range(self.pointerLength()):
            li.append(self.pointer[index])
        return li

    def __scan(self) -> Dict[int, List[ElementLoader]]:
        layer = {}
        rootElementLoader = ElementLoader(self.pointer)
        self.__innerScan(layer, rootElementLoader)
        self.depth = -1
        return layer

    def __innerScan(self, layer: Dict[int, List[ElementLoader]], previousElementLoader: ElementLoader):
        if self.pointerHasChildren():
            self.depth += 1
            for child in self.getPointerChildren():
                childElementLoader = ElementLoader(child)
                childElementLoader.setParent(previousElementLoader)
                previousElementLoader.addChild(childElementLoader)
                if self.depth in layer.keys():
                    layer[self.depth].append(childElementLoader)
                else:
                    layer[self.depth] = [childElementLoader]
                self.pointer = child
                self.__innerScan(layer, childElementLoader)
            self.depth -= 1

    def getScanDiction(self) -> Dict[int, List[ElementLoader]]:
        return self.__scanDiction

    def getBeanLoaderList(self) -> List[ElementLoader]:
        li = []
        if 0 in self.getScanDiction():
            for elementLoader in self.getScanDiction()[0]:
                if elementLoader.element.tag == "bean":
                    li.append(elementLoader)
        return li

    def buildBean(self, loader: ElementLoader):
        bean = Bean()

        id = None
        name = None
        className = None

        element: ET.Element = loader.element
        bean.attrib = element.attrib
        id = getAttributeFromElement(element, 'id')
        name = getAttributeFromElement(element, 'name')
        className = getAttributeFromElement(element, 'class')

        childrenLoaders = loader.children
        args = []
        for childLoader in childrenLoaders:
            childElement: ET.Element = childLoader.element
            if childElement.tag == "constructor-arg":
                args.append(childElement.attrib['value'])
            if childElement.tag == "property":
                pn = getAttributeFromElement(childElement, 'name')
                pf = getAttributeFromElement(childElement, 'ref')
                pv = getAttributeFromElement(childElement, 'value')
                prop = Property(
                    name=pn,
                    ref=pf,
                    value=pv,
                )
                bean.add_property(prop)

        try:
            bean.create(className, *args, application=self)
        except TypeError as e:
            se = str(e)
            if "missing" in se and "required positional arguments" in se:
                msg = se + "\n Maybe you forgot to use <constructor-arg/> ."
                raise TypeError(msg)

        return bean

    def getBean(self, arg) -> object:
        li = []
        beanELoader = None
        for beanELoader in self.getBeanLoaderList():
            if arg in beanELoader.element.attrib.values():
                li.append(self.buildBean(beanELoader))
        if len(li) > 1:
            for bean in li:
                if bean.attrib['id'] == arg:
                    return bean.instance
            raise KeyError("Too many results -> " + str(li))
        elif len(li) == 0:
            raise KeyError("Result not found")
        return li[0].instance
