import math

from demosys.effects import effect
from demosys import geometry


class Empty(effect.Effect):

    def __init__(self):
        self.shader = self.get_shader("shader.glsl", local=True)
        self.vao = geometry.quad_fs()
        self.texture1 = self.get_texture("WarpspeedTexture.jpg", local=True)
        self.texture2 = self.get_texture("WarpspeedTexture2.jpg", local=True)

        self.zangle = 0.0

    @effect.bind_target
    def draw(self, time, frametime, target):
        self.texture1.use(location=0)
        self.shader.uniform("tex", 0)
        self.texture2.use(location=1)
        self.shader.uniform("tex2", 1)

        self.shader.uniform("scroll", time * 1.5)
        self.shader.uniform("intensity", 1.0 + ((math.sin(time / 2)) / 2))
        self.shader.uniform("zangle", time)
        self.shader.uniform("speedlayer_alpha", (math.sin(time) + 1.0) / 2)
        self.shader.uniform("accelerate", 0.5)

        self.vao.draw(self.shader)
