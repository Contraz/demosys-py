import numpy
from pyrr import matrix44

import moderngl
from demosys.opengl.vao import VAO

from .base import BaseText, FontMeta


class TextWriter2D(BaseText):
    runnable = False

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
        self._config = self.get_data('demosys.program.font_meta')
        self._texture = self.get_texture('demosys.text.font_texture')
        self._program = self.get_program('demosys.text.program_writer_2d')

        self._string_buffer = None

        self._init(FontMeta(self._config))

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
        self._string_buffer.clear(chunk=b'\32')

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
                self._translate_string(text.encode('iso-8859-1', errors='replace'), self.area[0]),
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
        self._program["m_proj"].write(self._projection_bytes)
        self._program["text_pos"].value = cpos
        self._program["font_texture"].value = 0
        self._program["char_size"].value = csize
        self._program["line_length"].value = self.area[0]

        self._vao.render(self._program, instances=length)
