from demosys.test.testcase import DemosysTestCase
from demosys.effects.registry import effects
from demosys.scene import camera


class EffectTestCase(DemosysTestCase):

    @classmethod
    def setup_class(cls):
        effects.polulate(['tests.effect_package'])
        cls.effect = cls.project.create_effect("test", 'TestEffect')

    def test_properties(self):
        self.assertEqual(self.effect.name, 'tests.effect_package.effects.TestEffect')
        self.assertEqual(self.effect.label, 'test')

        self.assertEqual(self.effect.window, self.window)
        self.assertEqual(self.effect.ctx, self.ctx)
        self.assertIsInstance(self.effect.sys_camera, camera.SystemCamera)

    def test_methods(self):
        self.effect.post_load()
        self.effect.draw(0, 0, None)

    # def test_resources(self):
    #     self.assertIsNotNone(self.effect.get_program('vf_pos.glsl'))
    #     self.assertIsNotNone(self.effect.get_texture('crate.jpg'))
    #     self.assertIsNotNone(self.effect.get_scene('BoxTextured/glTF/BoxTextured.gltf'))
    #     self.assertIsNotNone(self.effect.get_data('data.txt', mode="text"))

    def test_misc_methods(self):
        self.effect.create_projection()
        self.effect.create_transformation()
