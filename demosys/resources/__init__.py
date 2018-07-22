from .shaders import shaders
from .textures import textures
from .tracks import tracks
from .scenes import scenes
from .data import data
from .data import Data  # noqa

ON_LOAD_FUNCS = []

__all__ = [
    'shaders',
    'textures',
    'tracks',
    'scenes',
    'data',
    'Data',
    'load',
    'count',
    'on_loaded',
]


def load():
    scenes.load()
    shaders.load()
    textures.load()
    tracks.load()
    data.load()

    for func in ON_LOAD_FUNCS:
        func()


def count():
    return shaders.count + textures.count


def on_loaded(func):
    ON_LOAD_FUNCS.append(func)
