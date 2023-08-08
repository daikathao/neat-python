from pyglet.image import load
import os


def get_sprite_map():
    this_dir = os.path.dirname(__file__)
    path = this_dir + "/assets/images/sprites.png"
    return load(os.path.abspath(path))
