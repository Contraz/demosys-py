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


class States:
    on_loaded_funcs = []
    on_load_funcs = []
    loaded = False

    @classmethod
    def sort_callbacks(cls):
        cls.on_load_funcs = sorted(cls.on_load_funcs, key=lambda x: x[0])
        cls.on_loaded_funcs = sorted(cls.on_loaded_funcs, key=lambda x: x[0])


def load():
    States.sort_callbacks()

    for func in reversed(States.on_load_funcs):
        func[1]()

    scenes.load()
    shaders.load()
    textures.load()
    tracks.load()
    data.load()

    States.loaded = True
    for func in reversed(States.on_loaded_funcs):
        func[1]()


def count():
    return shaders.count + textures.count


def loading_complete():
    return States.loaded


def on_load(func, priority=0):
    States.on_load_funcs.append((priority, func))


def on_loaded(func, priority=0):
    if loading_complete():
        func()
        return

    States.on_loaded_funcs.append((priority, func))
