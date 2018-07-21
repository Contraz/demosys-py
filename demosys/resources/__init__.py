from .shaders import shaders
from .textures import textures
from .tracks import tracks
from .scenes import scenes
from .data import data
from .data import Data  # noqa


def load():
    scenes.load()
    shaders.load()
    textures.load()
    tracks.load()
    data.load()


def count():
    return shaders.count + textures.count
