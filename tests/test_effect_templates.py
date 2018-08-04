import os

from demosys.test import DemosysTestCase
from demosys.effects.registry import effects
from demosys.effects import Effect
from demosys.scene import camera


class EffectTemplateTestCase(DemosysTestCase):

    def test_templates(self):
        templates = self.list_effect_templates()
        effects.polulate(templates)

        Effect.ctx = self.ctx
        Effect.window_aspect = 16 / 9
        Effect.window_width = self.window.width
        Effect.window_height = self.window.height
        Effect.sys_camera = camera.SystemCamera()

        for name, config in effects.effects.items():
            effect = config.cls()
            effect.post_load()
            effect.draw(0.0, 1 / 60, self.window.fbo)

            self.window.fbo.clear()

    def list_effect_templates(self):
        dirs = os.listdir(
            os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                'demosys',
                'effect_templates'
            )
        )
        return ["demosys.effect_templates.{}".format(d) for d in dirs]
