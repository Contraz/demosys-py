import os
from unittest import TestCase

os.environ['DEMOSYS_SETTINGS_MODULE'] = 'tests.settings'  # noqa

import demosys
from demosys import context, resources
from demosys.resources.meta import (
    TextureDescription,
    SceneDescription,
    ProgramDescription,
    DataDescription,
)

demosys.setup()
demosys.create_window().use()


class DemosysTestCase(TestCase):

    window = context.window()
    ctx = context.ctx()

    def load_program(self, path):
        return resources.programs.load(ProgramDescription(path=path))

    def load_texture(self, path):
        return resources.textures.load(TextureDescription(path=path))

    def load_texture_array(self, path, layers=0):
        return resources.textures.load(TextureDescription(path=path, loader='array', layers=layers))

    def load_scene(self, path):
        return resources.scenes.load(SceneDescription(path=path))

    def load_data(self, path, loader=None):
        return resources.data.load(DataDescription(path=path, loader=loader))

    def get_track(self, name):
        return resources.tracks.get(name)
