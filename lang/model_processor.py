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
    'color': 'black',
    'fps': 60,
    'movespeed': 6
}


def set_default_settings(model):
    print('we here')
    if not model.settings:
        model.settings = {}
    for key, value in defaults.items():
        if not key in model.settings:
            model.settings[key] = value


def pygame_sl_model_processor(model, metamodel):
    
    for item in model.items:
        print(item)

    for level in model.levels:
        print(level)

    # for setting in model.settings:
    #     print(setting)

    set_default_settings(model)
