from typing import List

from PyBean.instance import create_instance


class Property:
    def __init__(self, name, ref, value):
        self.name: str = name
        self.ref: str = ref
        self.value: object = value


class Bean:
    def __init__(self):
        self.attrib = {}
        self.instance = None
        self.__properties: List[Property] = []

    def add_property(self, prop: Property):
        self.__properties.append(prop)

    def get_properties(self) -> List[Property]:
        return self.__properties

    def create(self, class_name, *args, application):
        self.instance = create_instance(class_name, *args)
        for prop in self.__properties:
            if prop.value is not None:
                value = prop.value
                value_translate(value)
                exec(f"self.instance.{prop.name} = value")
            if prop.ref is not None:
                instance = application.getBean(prop.ref)
                prop.value = instance
                exec(f"self.instance.{prop.name} = instance")


def value_translate(value):
    if value.isdigit():
        value = int(value)
    elif "." in value:
        try:
            value = float(value.strip())
        except ValueError as e:
            pass
    return value
