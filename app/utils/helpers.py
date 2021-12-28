import json
import os


class SingleInstanceMetaClass(type):
    """
        https://www.pythonprogramming.in/singleton-class-using-metaclass-in-python.html
    """

    def __init__(self, name, bases, dic):
        self.__single_instance = None
        super().__init__(name, bases, dic)

    def __call__(cls, *args, **kwargs):
        if cls.__single_instance:
            return cls.__single_instance
        single_obj = cls.__new__(cls)
        single_obj.__init__(*args, **kwargs)
        cls.__single_instance = single_obj
        return single_obj


def get_env_variable(variable, json_dict, type_hint=None):
    value = os.getenv(variable, None)
    if not value:
        value = json_dict.get(variable, None)
    if value and type_hint:
        value = type_hint(value)
    return value
