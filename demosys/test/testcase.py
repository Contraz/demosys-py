from unittest import TestCase

import demosys
from demosys import context, resources
from demosys.opengl import ShaderProgram, TextureArray
from demosys.view import controller

demosys.setup()
controller.create_window()


class DemosysTestCase(TestCase):
    window = context.window()

    def create_shader(self, source):
        program = ShaderProgram(name="test")
        program.set_source(source)
        return program

    def get_shader(self, path):
        return resources.shaders.get(path, create=True)

    def get_texture(self, path):
        return resources.textures.get(path, create=True)

    def get_texture_array(self, path, layers=0):
        return resources.textures.get(path, create=True, cls=TextureArray, layers=layers)

    def get_track(self, name):
        return resources.tracks.get(name)
