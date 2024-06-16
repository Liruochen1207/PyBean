from typing import List

from PyBean.instance import create_instance

class Property:
    def __init__(self, name, ref, value):
        self.name = name
        self.ref = ref
        self.value = value


class Bean:
    def __init__(self):
        self.attrib = {}
        self.instance = None
        self.__properties: List[Property] = []

    def add_property(self, prop: Property):
        self.__properties.append(prop)

    def create(self, class_name, *args, application):
        self.instance = create_instance(class_name, *args)
        for prop in self.__properties:
            if prop.value is not None:
                exec(f"self.instance.{prop.name} = {prop.value}")
            if prop.ref is not None:
                instance = application.getBean(prop.ref)
                exec(f"self.instance.{prop.name} = instance")



