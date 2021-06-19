import os
from textx.metamodel import metamodel_from_file
from textx.export import metamodel_export

if __name__ == '__main__':
    pygame_sl_mm = metamodel_from_file(
        os.path.join(os.path.dirname(__file__), 'pygame_sl.tx'), debug=True
    )
else:
    from pygame_sl.lang.model_processor import pygame_sl_model_processor
    pygame_sl_mm = metamodel_from_file(os.path.join(os.path.dirname(__file__), 'pygame_sl.tx'))
    pygame_sl_mm.register_model_processor(pygame_sl_model_processor)
