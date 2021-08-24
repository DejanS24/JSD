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
from generator.util import python_module_name


def generate(model):
    # output_folder = target.output

    output_folder = "./outputs/"

    # Provera da li postoji generisan fajl sa tim imenom

    def animation_level(avatar):
        animation_lvl = ''
        if avatar.walkingImage:
            animation_lvl += 'walk '
        if avatar.idleImage:
            animation_lvl += 'idle '
        if avatar.jumpingImage:
            animation_lvl += 'jump '

        return animation_lvl

    def check_list(items, item_type):
        for i in items:
            if i.__class__.__name__ == item_type:
                return True
        return False

    def check_boosts(items):
        return check_list(items, 'Boost')

    def check_points(items):
        return check_list(items, 'Point')

    def check_sounds(sounds):
        if sounds is None: return False
        return sounds.jump_sound or sounds.boost_sound or sounds.point_sound

    def check_game_music(sounds):
        return sounds and sounds.game_music

    def check_end_music(sounds):
        return sounds and sounds.end_music

    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(join(dirname(__file__))))
    jinja_env.filters['animation_level'] = animation_level
    jinja_env.filters['check_boosts'] = check_boosts
    jinja_env.filters['check_points'] = check_points
    jinja_env.filters['check_sounds'] = check_sounds
    jinja_env.filters['check_game_music'] = check_game_music
    jinja_env.filters['check_end_music'] = check_end_music
    template = jinja_env.get_template('pygame.template')
    with open(join(output_folder, python_module_name(model.name)), 'w') as f:
        f.write(template.render(m=model))
