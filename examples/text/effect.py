import moderngl
from demosys.effects import effect
from demosys.text import TextWriter2D
# from pyrr import matrix44


class TextEffect(effect.Effect):

    def __init__(self):
        super().__init__()
        self.writer = TextWriter2D(
            (10, 1),
            aspect_ratio=self.window_aspect,
            text="Hello world! Hello world! Hello world!",
        )

    def post_load(self):
        pass

    @effect.bind_target
    def draw(self, time, frametime, target):
        self.ctx.disable(moderngl.CULL_FACE)

        self.writer.draw((0.02, 0.01), size=0.05)
