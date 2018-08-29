import moderngl
from demosys.test.testcase import DemosysTestCase
from demosys import geometry
from demosys.opengl.vao import VAO


class VAOTest(DemosysTestCase):

    def test_create(self):
        shader = self.load_program("vf_pos.glsl")
        vao = VAO("test")
        vao.buffer(
            self.ctx.buffer(reserve=12),
            '3f',
            "in_position",
        )
        vao.render(shader)

    def test_transform(self):
        shader = self.load_program("v_write_1.glsl")
        vao = VAO("transform", mode=moderngl.POINTS)
        vao.buffer(
            self.ctx.buffer(reserve=12),
            '1u',
            'in_val',
        )
        result = self.ctx.buffer(reserve=12)
        vao.transform(shader, result)
        self.assertEqual(
            result.read(),
            b'\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00',
        )

    def test_instanced(self):
        shader = self.load_program("vf_instanced.glsl")
        vao = geometry.cube(1.0, 1.0, 1.0)
        vao.buffer(
            self.ctx.buffer(reserve=4 * 10),
            '1f',
            "in_instance",
            per_instance=True,
        )
        vao.render(shader, instances=10)
