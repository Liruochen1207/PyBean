import xml.etree.ElementTree as ET

from PyBean.bean import Bean, create_instance


class Application:
    def __init__(self, applicationContextPath: str):
        self.tree = ET.parse(applicationContextPath)
        self.root = self.tree.getroot()


    def getBean(self, id):

        for child in self.root:
            attr = child.attrib
            if attr['id'] == id:
                bean = Bean(id)
                bean.attributes = attr
                class_name = attr['class']
                instance = create_instance(class_name)
                bean.instance = instance
                return bean
        raise AttributeError('No such bean')

    def matchBean(self, attrName, bean):
        for child in bean.attributes:
            if child == attrName:
                return self.getBean(bean.attributes[child])


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
