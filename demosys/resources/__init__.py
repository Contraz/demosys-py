from .shaders import shaders
from .textures import textures
from .tracks import tracks  # noqa
from .scenes import scenes
from .data import data, Data  # noqa


def load():
    scenes.load_pool()
    shaders.load_pool()
    textures.load_pool()
    data.load_pool()


def count():
    return scenes.count + shaders.count + textures.count + data.count
