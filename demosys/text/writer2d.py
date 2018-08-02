import numpy

import moderngl
from demosys.opengl import VAO, TextureArray
from demosys import resources
from pyrr import matrix44

from .base import BaseText, Meta


class TextWriter2D(BaseText):

    def __init__(self, area, text_lines=None, aspect_ratio=1.0):
        """
        :param area: (x, y) Text area size (number of characters)
        :param size: Text size
        :param text: Initial text lines
        """
        super().__init__()
        self.area = area
        self._text_lines = text_lines

        self._projection_bytes = None
        self._aspect_ratio = 1.0
        self.aspect_ratio = aspect_ratio

        self._vao = None
        self._texture = resources.textures.load('demosys/text/VeraMono.png', cls=TextureArray, layers=190)
        self._shader = resources.shaders.load('demosys/text/textwriter2d.glsl')
        self._config = resources.data.load('demosys/text/meta.json')

        self._string_buffer = None

        self._init(Meta(self._config.data))

        self._string_buffer = self.ctx.buffer(reserve=self.area[0] * 4 * self.area[1])
        self._string_buffer.clear(chunk=b'\32')
        pos = self.ctx.buffer(data=bytes([0] * 4 * 3))

        self._vao = VAO("textwriter", mode=moderngl.POINTS)
        self._vao.buffer(pos, '3f', 'in_position')
        self._vao.buffer(self._string_buffer, '1u', 'in_char_id', per_instance=True)

        self.text_lines = self._text_lines

    @property
    def text_lines(self):
        return self._text_lines

    @text_lines.setter
    def text_lines(self, value):
        self._text_lines = value

        for i, line in enumerate(self._text_lines):
            self.set_text_line(i, line)

    @property
    def aspect_ratio(self):
        return self._aspect_ratio

    @aspect_ratio.setter
    def aspect_ratio(self, value):
        self._aspect_ratio = value
        self._projection_bytes = matrix44.create_orthogonal_projection_matrix(
            -self.aspect_ratio,  # left
            self.aspect_ratio,  # right
            -1.0,  # bottom
            1.0,  # top
            -100.0,  # near
            100.0,  # far
            dtype=numpy.float32,
        ).tobytes()

    def set_text_line(self, line, text):
        if line >= self.area[1]:
            return

        self._string_buffer.clear(size=self.area[0] * 4, offset=self.area[0] * 4 * line, chunk=b'\32')

        self._string_buffer.write(
            numpy.fromiter(
                self._translate_string(text.encode('iso-8859-1'), self.area[0]),
                dtype=numpy.uint32
            ).tobytes(),
            offset=(self.area[0] * 4) * line,
        )

    def draw(self, pos, length=-1, size=1.0):
        if length < 0:
            length = self.area[0] * self.area[1]
        elif length > self.area[0] * self.area[1]:
            length = self.area[0] * self.area[1]

        csize = (
            self._meta.character_width / self._meta.character_height * size,
            1.0 * size,
        )

        cpos = (
            pos[0] - self._aspect_ratio + csize[0] / 2,
            -pos[1] + 1.0 - csize[1] / 2,
        )

        self._texture.use(location=0)
        self._shader.uniform("m_proj", self._projection_bytes)
        self._shader.uniform("text_pos", cpos)
        self._shader.uniform("font_texture", 0)
        self._shader.uniform("char_size", csize)
        self._shader.uniform("line_length", self.area[0])

        self._vao.draw(self._shader, instances=length)
