import os
from unittest import TestCase

os.environ['DEMOSYS_SETTINGS_MODULE'] = 'tests.settings'  # noqa

import demosys
from demosys import context, resources
from demosys.opengl import ShaderProgram, TextureArray
from demosys.view import controller

demosys.setup()
controller.create_window()


class DemosysTestCase(TestCase):

    window = context.window()
    ctx = context.ctx()

    def create_shader(self, source=None, path=None):
        """
        Create a shader from source or file
        """
        program = ShaderProgram(name="test", path=path)

        if source:
            program.set_source(source)
            program.prepare()

        if path:
            resources.shaders.load_shader(program)

        return program

    def get_texture(self, path):
        return resources.textures.get(path, create=True)

    def get_texture_array(self, path, layers=0):
        return resources.textures.get(path, create=True, cls=TextureArray, layers=layers)

    def get_track(self, name):
        return resources.tracks.get(name)
