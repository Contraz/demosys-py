import os
from unittest import TestCase

import demosys
from demosys import context, resources
from demosys.resources.meta import (
    TextureDescription,
    SceneDescription,
    ProgramDescription,
    DataDescription,
)


class DemosysTestCase(TestCase):

    window = context.window()
    ctx = context.ctx()

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
