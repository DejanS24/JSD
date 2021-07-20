from textx.exceptions import TextXSemanticError
# from pygame_sl.generator import generator

colors = [
    "black",
    "blue",
    "red",
    "green",
    "yellow",
    "white"
]

# default values if none is given in .pg file
defaults = {
    'screen_width': 800,
    'screen_height': 600,
    'font': 'arial',
    'default_color': 'black',
    'fps': 60,
    'movespeed': 6,
    'default_texture_color': 'green'
}


def check_color_existing(key, value):
     return key.__contains__('color') and value not in colors


def set_default_settings(model):
    print('we here')
    if not model.settings:
        model.settings = {}
    for key, value in defaults.items():
        attr_val = getattr(model.settings, key)

        if len(attr_val) == 0 and not check_color_existing(key, attr_val):
            setattr(model.settings, key, value)
        else:
            setattr(model.settings, key, attr_val[0])


def pygame_sl_model_processor(model, metamodel):
    
    for item in model.items:
        print(item)

    for level in model.levels:
        print(level)

    set_default_settings(model)
