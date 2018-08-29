import sys
from unittest import TestCase
from unittest.mock import MagicMock

from demosys import context, resources
from demosys import project
from demosys.resources.meta import (
    TextureDescription,
    SceneDescription,
    ProgramDescription,
    DataDescription,
)

MOCK_MODULES = ['glfw', 'pyglet', 'pyglet.window']


def apply_mocks():
    # Mock modules
    class Mock(MagicMock):
        @classmethod
        def __getattr__(cls, name):
            return MagicMock()

    sys.modules.update((mod_name, Mock()) for mod_name in MOCK_MODULES)


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
