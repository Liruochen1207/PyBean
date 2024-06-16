import xml.etree.ElementTree as ET
from typing import Dict, List

from PyBean.bean import Bean
from PyBean.by import *


def create_instance(class_name, *args):
    parts = class_name.split('.')
    module_name = '.'.join(parts[:-1])
    class_name = parts[-1]

    try:
        module = __import__(module_name, fromlist=[class_name])
        clazz = getattr(module, class_name)
        return clazz(*args)
    except ImportError as e:
        raise ImportError(f"Unable to import {module_name}: {e}")
    except AttributeError:
        raise AttributeError(f"Class {class_name} not found in {module_name}")
    except ValueError as e:
        print(e)


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

    def setParent(self, parent: ET.Element):
        self.parent = parent

    def addChild(self, child: ET.Element):
        self.children.append(child)


class Application:
    def __init__(self, applicationContextPath: str):
        self.tree = ET.parse(applicationContextPath)
        self.root = self.tree.getroot()
        self.pointer: ET.Element = self.root
        self.depth = -1
        self.__scanDiction: Dict[int, ElementLoader] = self.__scan()

    def pointerLength(self) -> int:
        return self.pointer.__len__()

    def pointerHasChildren(self) -> bool:
        return self.pointerLength() > 0

    def getPointerChildren(self) -> List[ET.Element]:
        li = []
        for index in range(self.pointerLength()):
            li.append(self.pointer[index])
        return li

    def __scan(self) -> Dict[int, ElementLoader]:
        layer = {}
        rootElementLoader = ElementLoader(self.pointer)
        self.__innerScan(layer, rootElementLoader)
        self.depth = -1
        return layer

    def __innerScan(self, layer: Dict[int, ElementLoader], previousElementLoader: ElementLoader):
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


    def getScanDiction(self) -> Dict[int, ElementLoader]:
        return self.__scanDiction


    def getBeanLoaderList(self) -> List[Bean]:
        li = []
        if 0 in self.getScanDiction():
            for elementLoader in self.getScanDiction()[0]:
                if elementLoader.element.tag == "bean":
                    li.append(elementLoader)
        return li


    def getBean(self) -> object:
        loader: ElementLoader = self.getBeanLoaderList()[0]
        childrenLoaders = loader.children

        element = loader.element
        print(element.attrib)
        return create_instance(element.attrib['class'], "hi")