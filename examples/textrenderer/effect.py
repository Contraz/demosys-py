import math
import os

from demosys.effects import effect
from demosys.text import TextRenderer2D


class TextRendererEffect(effect.Effect):

    def __init__(self):
        super().__init__()

        with open(os.path.join(os.path.dirname(__file__), 'sample.txt'), 'r') as fd:
            lines = fd.readlines()

        self.renderer = TextRenderer2D(
            (105, len(lines)),
            text_lines=lines,
            texture_height=8192,
        )

    def post_load(self):
        self.renderer.render()

    def draw(self, time, frametime, target):
        self.renderer.draw(
            (0.05, math.fmod(time, 75.0) / 5.0),
            size=0.75,
        )
