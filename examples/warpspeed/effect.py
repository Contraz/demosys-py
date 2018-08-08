import math

from demosys.effects import effect
from demosys import geometry


class Empty(effect.Effect):

    def __init__(self):
        self.vao = geometry.quad_fs()
        self.program = self.get_program("shader")
        self.texture1 = self.get_texture("WarpspeedTexture")
        self.texture2 = self.get_texture("WarpspeedTexture2")

        self.zangle = 0.0

    def draw(self, time, frametime, target):
        self.texture1.use(location=0)
        self.program.uniform("tex", 0)
        self.texture2.use(location=1)
        self.program.uniform("tex2", 1)

        self.program.uniform("scroll", time * 1.5)
        self.program.uniform("intensity", 1.0 + ((math.sin(time / 2)) / 2))
        self.program.uniform("zangle", time)
        self.program.uniform("speedlayer_alpha", (math.sin(time) + 1.0) / 2)
        self.program.uniform("accelerate", 0.5)

        self.vao.draw(self.program)
