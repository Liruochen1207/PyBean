import os
import xml.etree.ElementTree as ET
from typing import Dict, List

from PyBean.bean import Bean, Property, value_translate
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


class ApplicationMode:
    release = 0
    default = 1
    development = 2
    debug = 3
    test = 4

    def parse_mode(self, inp: str):
        if inp.isdigit():
            return int(inp)
        if inp.lower() == 'release':
            return self.release
        if inp.lower() == 'default':
            return self.default
        if inp.lower() in ('dev', 'development'):
            return self.development
        if inp.lower() == 'debug':
            return self.debug
        if inp.lower() == 'test':
            return self.test



class ApplicationContext:
    def __init__(self, applicationContextPath: str, applicationMode=ApplicationMode.default):

        applicationContextPath = os.path.abspath(applicationContextPath)
        self.dirPath = os.path.dirname(applicationContextPath)

        self.tree = None
        self.root = None
        self.pointer = None
        self.depth = None
        self.__scanDiction = None
        self.childApplications = []

        self.__mode = applicationMode

        self.path = applicationContextPath
        self.reloadFromfile()
        self.refresh()  # Init
        self.__doImportLoadList()

    def debug_print(self, *args, **kwargs):
        if self.__mode in (ApplicationMode.debug, ApplicationMode.test, ApplicationMode.development):
            print(self.path.split('\\')[-1] + " -> ", end='')
            print(*args, **kwargs)

    def pointerLength(self) -> int:
        return self.pointer.__len__()

    def pointerHasChildren(self) -> bool:
        return self.pointerLength() > 0

    def getPointerChildren(self) -> List[ET.Element]:
        li = []
        for index in range(self.pointerLength()):
            li.append(self.pointer[index])
        return li

    def reloadFromfile(self):
        self.debug_print('reloadFromfile')
        self.tree = ET.parse(self.path)
        self.root = self.tree.getroot()
        self.pointer: ET.Element = self.root
        self.depth = -1

    def refresh(self):
        self.debug_print('refresh')
        self.__scanDiction: Dict[int, List[ElementLoader]] = self.__scan()
    
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

    def __getLoaderList(self, depth: int, tagName: str) -> List[ElementLoader]:
        li = []
        if depth in self.getScanDiction():
            for elementLoader in self.getScanDiction()[depth]:
                if elementLoader.element.tag == tagName:
                    li.append(elementLoader)
        return li

    def getImportLoadList(self) -> List[ElementLoader]:
        return self.__getLoaderList(depth=0, tagName='import')

    def __doImportLoadList(self):
        for loader in self.getImportLoadList():
            element = loader.element

            resource = getAttributeFromElement(element, 'resource')
            readyPath = self.dirPath+"\\"+resource
            if not os.path.exists(readyPath):
                readyPath = resource
            childApplication = ApplicationContext(applicationContextPath=readyPath, applicationMode=self.__mode)
            self.childApplications.append(childApplication)

    def getBeanLoaderList(self) -> List[ElementLoader]:
        li = []
        for childApplication in self.childApplications:
            li.extend(childApplication.getBeanLoaderList())
        li.extend(self.__getLoaderList(depth=0, tagName="bean"))
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
                if "value" in childElement.attrib:
                    value = childElement.attrib['value']
                    value_translate(value)
                    args.append(value)

                elif "ref" in childElement.attrib:
                    ref = childElement.attrib['ref']
                    value = self.getBean(ref)
                    args.append(value)

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
            # print(e)
            se = str(e)
            if "missing" in se and "required" in se:
                msg = se + f"\n Maybe you forgot to use <constructor-arg/> or delete this argument from {className}."
                raise TypeError(msg)
            raise e

        return bean

    def getBean(self, arg) -> object:
        if self.__mode == ApplicationMode.development:
            self.reloadFromfile()
            self.refresh()
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
            raise KeyError(f"Result '{arg}' not found")
        return li[0].instance
