from demosys.test import DemosysTestCase
import numpy


class ShaderTest(DemosysTestCase):

    def test_create(self):
        shader = self.create_shader(path='vf_pos.glsl')
        assert shader.mglo != None

    def test_general(self):
        shader = self.create_shader(path='vf_pos_color.glsl')
        shader.uniform("color", (1.0, 1.0, 1.0, 1.0))

        byte_data = numpy.array([1.0] * 4, dtype=numpy.dtype('f4')).tobytes()
        shader.uniform("color", byte_data)

        uniform = shader.uniform("color")
        uniform.write(byte_data)

        assert len(shader.attribute_key) > 0
        assert len(shader.attribute_list) == 1
        assert len(shader.attribute_map) == 1
