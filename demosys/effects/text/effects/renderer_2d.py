import numpy

import moderngl
from demosys.effects.text.effects import TextWriter2D
from demosys.opengl.vao import VAO


class TextRenderer2D(TextWriter2D):
    runnable = False

    def __init__(self, area, text_lines=None, texture_height=64):
        """
        :param area: (x, y) Text area size (number of characters)
        :param size: Text size
        :param text: Initial text
        """
        super().__init__(area, text_lines=text_lines)
        self._texture_height = texture_height
        self._texture_width = 0

        self._quad = self._create_vao()
        self._quad_program = self.get_program('demosys.text.program_renderer_2d')
        self._fbo = None

        self._texture_width = int(
            round(self._meta.char_aspect_wh * self._texture_height * self.area[0] / self.area[1], 0)
        )

        self.aspect_ratio = self._texture_width / self._texture_height
        self._fbo = self.ctx.framebuffer(self.ctx.texture((self._texture_width, self._texture_height), 4))
        self._fbo_scope = self.ctx.scope(self._fbo)

    @property
    def texture(self):
        return self._fbo.color_attachments[0]

    def render(self):
        self._fbo.clear()
        with self._fbo_scope:
            super().draw((0.0, 0.0), size=2.0 / self.area[1])

    def draw(self, pos, size=1.0):
        self._fbo.color_attachments[0].use(location=0)
        self._quad_program["texture0"].value = 0
        self._quad_program["yscale"].value = self._texture_height / self._texture_width
        self._quad_program["pos"].value = pos
        self._quad_program["size"].value = size
        self._quad.render(self._quad_program)

    def _create_vao(self):
        data = numpy.array([
            0.0, -2.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0, 1.0,
            2.0, 0.0, 0.0, 1.0, 1.0,
            0.0, -2.0, 0.0, 0.0, 0.0,
            2.0, 0.0, 0.0, 1.0, 1.0,
            2.0, -2.0, 0.0, 1.0, 0.0,
        ], dtype=numpy.float32)

        vao = VAO("textrenderer", mode=moderngl.TRIANGLES)
        vao.buffer(data, '3f 2f', ['in_position', 'in_uv'])
        return vao
