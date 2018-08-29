import os

from demosys.test.testcase import DemosysTestCase
from demosys.effects.registry import effects


class EffectTemplateTestCase(DemosysTestCase):

    def test_templates(self):
        templates = self.list_effect_templates()
        effects.polulate(templates)
        self.project.load()

        for template in templates:
            package = effects.get_package(template)
            for effect_cls in package.runnable_effects():
                effect = effect_cls()
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
