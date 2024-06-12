import xml.etree.ElementTree as ET

from PyBean.bean import Bean, create_instance
from PyBean.by import *


class Application:
    def __init__(self, applicationContextPath: str):
        self.tree = ET.parse(applicationContextPath)
        self.root = self.tree.getroot()
        self.attribList = []

    def refresh(self):
        self.attribList = []
        for child in self.root:
            attr = child.attrib
            self.attribList.append(attr)

    def clear(self):
        self.attribList = []

    def getBean(self, arg=Default, by=Default, requiredType=Default):
        self.refresh()
        def search(var):
            ready = []
            bean = Bean(arg)
            for attr in self.attribList:
                if attr[var] == arg and var != "class":

                    bean.attributes = attr
                    class_name = attr['class']
                    instance = create_instance(class_name)
                    bean.instance = instance

                    if requiredType == Default or type(bean.instance) == requiredType or requiredType in str(bean.instance):
                        return bean
                    else:
                        raise TypeError(f'{bean.instance} is not a {requiredType}.')

                if type(arg) == str and arg in str(attr[var]):

                    if len(ready) == 1:
                        raise SystemError(f'More than one bean {var} is required.')
                    instance = create_instance(attr[var])

                    bean.instance = instance
                    ready.append(bean)
            if len(ready) == 0:
                raise AttributeError(f'No such bean {var} as {arg}')
            else:
                return ready[0]



        if type(by) == str:
            arg = by
            by = By.id

        if by == Default and type(arg) == str:
            by = By.id

        if by == By.id:
            return search("id")
        if by == By.name:
            return search("name")
        if by == By.clazz:
            return search("class")

        if by == Default:

            if requiredType == Default:
                raise AttributeError(f'No such bean id as {arg}')
            else:
                arg = requiredType
                return search('class')




    def getBeanList(self):
        bean_list = []
        for child in self.root:
            attr = child.attrib
            bean = Bean(id)
            bean.attributes = attr
            class_name = attr['class']
            instance = create_instance(class_name)
            bean.instance = instance
            bean_list.append(bean)

        return bean_list
