import re


def python_module_name(name):
    return "%s.py" % re.sub(r'[^\w\.-]', '_', name.lower())
