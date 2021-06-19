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

default_screen_width = 800
default_screen_height = 600
default_font = "arial"
default_color = "black"
default_fps = 60


def pygame_sl_model_processor(model, metamodel):
    
    for item in model.items:
        print(item)

    for level in model.levels:
        print(level)

    for setting in model.settings:
        print(setting)
