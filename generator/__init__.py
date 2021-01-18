"""
pygame_sl code generator transforms pygame_sl game models into
python file.

"""

import os
from os.path import join, dirname, isdir, exists
import shutil
import jinja2
import datetime
import re
from pygame_sl.generator.util import python_module_name


def generate(model):

    # output_folder = target.output

    output_folder = "./outputs/"
    # Provera da li postoji generisan fajl sa tim imenom

    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(join(dirname(__file__))))
    template = jinja_env.get_template('pygame.template')
    with open(join(output_folder, python_module_name(model.name)), 'w') as f:
        f.write(template.render(m=model))
