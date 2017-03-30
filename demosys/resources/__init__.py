from .shaders import shaders
from .textures import textures


def load():
    shaders.load()
    textures.load()


def count():
    return shaders.count + textures.count
