from demosys.test import DemosysTestCase
from demosys.effects.registry import effects
from demosys.effects import Effect
from demosys.scene import camera


class EffectTestCase(DemosysTestCase):

    def setUp(self):
        Effect._ctx = self.ctx
        Effect._window_width = self.window.width
        Effect._window_height = self.window.height
        Effect._window_aspect = self.window.width / self.window.height
        Effect._sys_camera = camera.SystemCamera()

        effects.polulate(['tests'])
        self.effect = effects.effects.get('tests.effect').cls()

    def test_properties(self):
        self.assertEqual(self.effect.name, 'tests')
        self.assertEqual(self.effect.window_width, self.window.width)
        self.assertEqual(self.effect.window_height, self.window.height)
        self.assertEqual(self.effect.window_size, self.window.size)
        self.assertEqual(self.effect.window_aspect, self.window.width / self.window.height)
        self.assertEqual(self.effect.ctx, self.ctx)
        self.assertIsInstance(self.effect.sys_camera, camera.SystemCamera)
        self.assertEqual(self.effect.effect_name, 'tests')

    def test_methods(self):
        self.effect.post_load()
        self.effect.draw(0, 0, None)

    def test_resources(self):
        self.assertIsNotNone(self.effect.get_shader('vf_pos.glsl'))
        self.assertIsNotNone(self.effect.get_texture('crate.jpg'))
        self.assertIsNotNone(self.effect.get_scene('BoxTextured/glTF/BoxTextured.gltf'))
        self.assertIsNotNone(self.effect.get_data('data.txt', mode="text"))

    def test_misc_methods(self):
        self.effect.create_projection()
        self.effect.create_transformation()
