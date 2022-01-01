import json
import os
import sys


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


def get_env_variable(variable, json_dict, type_hint=None, default_value=None):
    value = os.getenv(variable, None)
    if not value:
        value = json_dict.get(variable, None)
    if value and type_hint:
        value = type_hint(value)
    else:
        value = default_value
    return value


def remove_hidden_vars_fun_and_methods(dunder_dict):
    variables = []
    for key in dunder_dict:
        # if key is not None
        if key:
            # And key doesn't start with _ or __
            if not(key[0] == '_' or key[0:2] == '__'):
                # And key's value in the dict is not None
                if dunder_dict[key] is not None:
                    # And dunder_dict[key] doesn't have the string 'function' or 'classmethod' in it
                    if not ('function' in str(dunder_dict[key]) or 'classmethod' in str(dunder_dict[key]) or 'staticmethod' in str(dunder_dict[key])):
                        # Then, it is a variable
                        variables.append(key)
                # If key's value is None, then it can't be a function/method, so it too must be a variable
                else:
                    # Then too, it is a variable
                    variables.append(key)
    return variables


def pretty_text(class_name, key_value_dict, boundary, boundary_length, separator, indentation_text):
    text = [f"{indentation_text}{key}: {value}" for key,
            value in key_value_dict.items()]
    text.insert(0, boundary * boundary_length)
    text.insert(0, class_name)
    text.insert(0, boundary * boundary_length)
    text.append(boundary * boundary_length)
    text = f"{separator}".join(text)
    return text


def prompt(prompt):
    sys.stdout.write(prompt + ": ")
    sys.stdout.flush()
    return sys.stdin.readline().strip()
