from textx import language
from .pglang import pygame_sl_mm


@language('pygame_sl', '*.pg')
def pygame_sl_lang():
    return pygame_sl_mm
