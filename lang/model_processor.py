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


def pygame_sl_model_processor(model, metamodel):
    
    for item in model.items:
        print(item)

    for level in model.levels:
        print(level)
