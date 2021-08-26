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
    if key.__contains__('color'):
        if value not in colors:
            return True
        else:
            return False
    else:
        return False


def set_default_settings(model):
    if not model.settings:
        model.settings = {}

    for key, value in defaults.items():
        try:
            attr_val = getattr(model.settings, key)
        except AttributeError:
            model.settings[key] = value
            continue

        if len(attr_val) == 0 or check_color_existing(key, attr_val[0]):
            setattr(model.settings, key, value)
        else:
            setattr(model.settings, key, attr_val[0])


def pygame_sl_model_processor(model, metamodel):
    
    for item in model.items:
        print(item)
        if item.avatar.__class__.__name__ == 'Color' and check_color_existing('color', item.avatar.color):
            item.avatar.color = defaults['default_texture_color']

    for level in model.levels:
        print(level)

    set_default_settings(model)
