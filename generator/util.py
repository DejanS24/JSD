from random import sample
import re


def flatten_structure(model):

    elements = model.structure.elements

    def _flatten(elements):
        instances = []
        for e in elements:
            if e.__class__.__name__ == "Sequence":
                instances.extend(_flatten(e.elements))
            elif e.__class__.__name__ == "Randomize":
                # Randomize contained elements
                instances.extend(_flatten(
                    sample(e.elements, len(e.elements))))
            else:
                # It must be an instance
                instances.append(e)
        return instances

    return _flatten(elements)


def python_module_name(name):

    return "%s.py" % re.sub(r'[^\w\.-]', '_', name.lower())
