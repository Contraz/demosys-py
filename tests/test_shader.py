import numpy

import moderngl
from demosys.test import DemosysTestCase


class ShaderTest(DemosysTestCase):

    def test_create(self):
        shader = self.create_shader(path='vf_pos.glsl')
        assert shader.mglo != None

    def test_uniforms(self):
        path = 'vf_pos_color.glsl'
        shader = self.create_shader(path='vf_pos_color.glsl')
        self.assertAttributes(shader)

        byte_data = numpy.array([1.0] * 4, dtype=numpy.dtype('f4')).tobytes()
        shader.uniform("color", (1.0, 1.0, 1.0, 1.0))
        shader.uniform("color", byte_data)
        shader['color'].write(byte_data)

        uniform = shader.uniform("color")
        uniform.write(byte_data)

    def test_geometry_shader(self):
        shader = self.create_shader(path='vgf_quads.glsl')
        self.assertAttributes(shader)

        assert shader.geometry_input == moderngl.POINTS
        assert shader.geometry_output == moderngl.TRIANGLE_STRIP
        assert shader.geometry_vertices == 4

    def assertAttributes(self, shader):
        assert shader.attribute_key
        assert len(shader.attribute_list) == 1
        assert len(shader.attribute_map) == 1
        assert shader.path in str(shader)
