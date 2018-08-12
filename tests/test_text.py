from demosys.test import DemosysTestCase
from demosys.effects.registry import effects


class TextTestCase(DemosysTestCase):
    """Crude test executing text code"""

    def setUp(self):
        effects.add_package('demosys.effects.text')
        self.project.load()

    def test_create(self):
        instance = self.project.create_effect(
            'TextWriter2D',
            'TextWriter2D',
            (4, 4),
            text_lines=[
                "ABCD",
                "!@#$",
                "abcd",
                "1234",
            ]
        )
        instance.draw((0, 0), size=1.0)
