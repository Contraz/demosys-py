from .shaders import shaders
from .textures import textures
from .tracks import tracks
from .scenes import scenes
from .data import data
from .data import Data  # noqa

__all__ = [
    'shaders',
    'textures',
    'tracks',
    'scenes',
    'data',
    'Data',
    'load',
    'count',
    'on_load',
    'on_loaded',
    'loading_complete',
]


def load():
    scenes.load_pool()
    shaders.load_pool()
    textures.load_pool()
    data.load_pool()


def count():
    return scenes.count + shaders.count + textures.count + data.count
