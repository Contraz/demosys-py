from demosys.test import DemosysTestCase
from demosys.opengl import VAO
from demosys import geometry


class VAOTest(DemosysTestCase):

    def test_create(self):
        shader = self.create_shader(path="vf_pos.glsl")
        vao = VAO("test")
        vao.buffer(
            self.ctx.buffer(reserve=12),
            '3f',
            "in_position",
        )
        vao.draw(shader)

    def test_transform(self):
        shader = self.create_shader(path="v_write_1.glsl")
        vao = VAO("transform")
        vao.buffer(
            self.ctx.buffer(reserve=12),
            '1u',
            'in_val',
        )
        result = self.ctx.buffer(reserve=12)
        vao.transform(shader, result)
        self.assertEqual(
            result.read(),
            b'\x01\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00',
        )

    def test_instanced(self):
        shader = self.create_shader(path="vf_instanced.glsl")
        vao = geometry.cube(1.0, 1.0, 1.0)
        vao.buffer(
            self.ctx.buffer(reserve=4 * 10),
            '1f',
            "in_instance",
            per_instance=True,
        )
        vao.draw(shader, instances=10)
