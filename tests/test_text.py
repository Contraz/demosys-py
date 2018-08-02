from demosys.test import DemosysTestCase
from demosys.text import TextWriter2D, TextRenderer2D


class TextTestCase(DemosysTestCase):

    def test_writer(self):
        writer = TextWriter2D(
            (4, 4),
            text_lines=[
                "ABCD",
                "!@#$",
                "abcd",
                "1234",
            ]
        )
        writer.draw((0, 0), size=1.0)

    def test_renderer(self):
        pass
