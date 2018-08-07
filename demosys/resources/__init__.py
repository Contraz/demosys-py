from demosys.resources.programs import programs, ProgramDescription  # noqa
from demosys.resources.textures import textures, TextureDescription  # noqa
from demosys.resources.tracks import tracks  # noqa
from demosys.resources.scenes import scenes, SceneDescription  # noqa
from demosys.resources.data import data, DataDescription  # noqa


def load():
    scenes.load_pool()
    programs.load_pool()
    textures.load_pool()
    data.load_pool()


def count():
    return scenes.count + programs.count + textures.count + data.count
