from demosys.effects import effect
from demosys.text import TextWriter2D


class TextEffect(effect.Effect):

    def __init__(self):
        self.writer = TextWriter2D((10, 1), text="Hello world!")

    @effect.bind_target
    def draw(self, time, frametime, target):
        self.writer.draw()
