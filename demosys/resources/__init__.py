from demosys.resources.programs import programs  # noqa
from demosys.resources.textures import textures  # noqa
from demosys.resources.tracks import tracks  # noqa
from demosys.resources.scenes import scenes  # noqa
from demosys.resources.data import data  # noqa


def load():
    scenes.load_pool()
    programs.load_pool()
    textures.load_pool()
    data.load_pool()


def count():
    return scenes.count + programs.count + textures.count + data.count
