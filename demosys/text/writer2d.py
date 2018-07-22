import numpy

import moderngl
from demosys.opengl import VAO, TextureArray
from demosys.resources import data, shaders, textures
from pyrr import matrix44

from .base import BaseText, Meta


class TextWriter2D(BaseText):

    def __init__(self, area, text="", aspect_ratio=1.0):
        """
        :param area: (x, y) Text area size (number of characters)
        :param size: Text size
        :param text: Initial text
        """
        super().__init__()
        self.area = area
        self._text = text.encode('latin1')

        self.projection_bytes = None
        self._aspect_ratio = 1.0
        self.aspect_ratio = aspect_ratio

        self._vao = None
        self._texture = textures.get('demosys/text/VeraMono.png', cls=TextureArray, layers=190, create=True)
        self._shader = shaders.get('demosys/text/textwriter2d.glsl', create=True)
        self._config = data.get('demosys/text/meta.json', create=True)

        data.on_loaded(self._post_load)

    def _post_load(self):
        """Parse font metadata after resources are loaded"""
        self._init(Meta(self._config.data))

        self._string_data = self._translate_data(self._text)
        self._string_buffer = self.ctx.buffer(
            data=numpy.array(self._string_data, dtype=numpy.uint32).tobytes()
        )
        self._pos = self.ctx.buffer(data=bytes([0] * 4 * 3))

        self._vao = VAO("textwriter", mode=moderngl.POINTS)
        self._vao.buffer(self._pos, '3f', 'in_position')
        self._vao.buffer(self._string_buffer, '1u', 'in_char_id', per_instance=True)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value

    @property
    def aspect_ratio(self):
        return self._aspect_ratio

    @aspect_ratio.setter
    def aspect_ratio(self, value):
        self._aspect_ratio = value
        self.projection_bytes = matrix44.create_orthogonal_projection_matrix(
            -self.aspect_ratio,  # left
            self.aspect_ratio,  # right
            -1.0,  # bottom
            1.0,  # top
            -100.0,  # near
            100.0,  # far
            dtype=numpy.float32,
        ).tobytes()

    def draw(self, pos, size=1.0):
        csize = (
            self._meta.character_width / self._meta.character_height * size,
            1.0 * size,
        )
        cpos = (
            pos[0] - self._aspect_ratio + csize[0] / 2,
            -pos[1] + 1.0 - csize[1] / 2,
        )

        self._texture.use(location=0)
        self._shader.uniform("m_proj", self.projection_bytes)
        self._shader.uniform("text_pos", cpos)
        self._shader.uniform("font_texture", 0)
        self._shader.uniform("char_size", csize)
        self._vao.draw(self._shader, instances=len(self._string_data))
