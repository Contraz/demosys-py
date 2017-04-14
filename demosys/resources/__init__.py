from .shaders import shaders
from .textures import textures
from .tracks import tracks


def load():
    shaders.load()
    textures.load()
    tracks.load()


def count():
    return shaders.count + textures.count
