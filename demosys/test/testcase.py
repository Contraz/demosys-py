from unittest import TestCase

from demosys import context, resources
from demosys import project
from demosys.resources.meta import (
    TextureDescription,
    SceneDescription,
    ProgramDescription,
    DataDescription,
)
from demosys.test.mocks import apply_mocks


class DemosysTestCase(TestCase):

    window = context.window()
    ctx = context.ctx()
    project = project.instance
    timeline = None

    apply_mocks()

    def load_program(self, path):
        return resources.programs.load(ProgramDescription(label=path, path=path))

    def load_texture(self, path):
        return resources.textures.load(TextureDescription(label=path, path=path))

    def load_texture_array(self, path, layers=0):
        return resources.textures.load(TextureDescription(label=path, path=path, loader='array', layers=layers))

    def load_scene(self, path):
        return resources.scenes.load(SceneDescription(label=path, path=path))

    def load_data(self, path, loader=None):
        return resources.data.load(DataDescription(label=path, path=path, loader=loader))

    def get_track(self, name):
        return resources.tracks.get(name)
