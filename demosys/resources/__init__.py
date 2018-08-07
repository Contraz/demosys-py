from demosys.resources.programs import programs, Program  # noqa
from demosys.resources.textures import textures
from demosys.resources.tracks import tracks  # noqa
from demosys.resources.scenes import scenes
from demosys.resources.data import data, Data  # noqa


def load():
    scenes.load_pool()
    programs.load_pool()
    textures.load_pool()
    data.load_pool()


def count():
    return scenes.count + programs.count + textures.count + data.count
