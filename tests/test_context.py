import moderngl

from demosys.test.testcase import DemosysTestCase
from demosys import geometry


class ContextTestCase(DemosysTestCase):
    """Test the headless context/window"""

    def test_properties(self):
        self.assertEqual(type(self.window.ctx), moderngl.Context)
        # We don't have a default framebuffer in headless mode
        self.assertIsNone(self.ctx.screen)
        self.assertIsNotNone(self.window.fbo)

    def test_basic_render(self):
        """Ensure we actually draw something to the screen"""
        vao = geometry.quad_fs()
        program = self.load_program(path='vf_pos_color.glsl')
        program["color"].value = (1.0, 1.0, 1.0, 1.0)
        vao.render(program)

        data = self.window.fbo.read()
        self.assertEqual(data[:10], b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff')
