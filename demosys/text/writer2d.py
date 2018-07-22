import numpy
import moderngl
from demosys.opengl import VAO
from demosys.resources import data, shaders, textures
from demosys.opengl import TextureArray

from .base import BaseText, Meta


class TextWriter2D(BaseText):

    def __init__(self, area, size=0.1, text=""):
        """
        :param area: (x, y) Text area size (number of characters)
        :param size: Text size
        :param text: Initial text
        """
        super().__init__()
        self.area = area
        self.size = size
        self._text = text.encode('latin1')

        self._vao = None
        self._texture = textures.get('demosys/text/VeraMono.png', cls=TextureArray, layers=190, create=True)
        self._shader = shaders.get('demosys/text/textwriter.glsl', create=True)
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

    def draw(self, proj_matrix, view_matrix):
        # print(self._text, self._string_data)
        self._texture.use(location=0)
        self._shader.uniform("m_proj", proj_matrix.astype('f4').tobytes())
        self._shader.uniform("m_mv", view_matrix.astype('f4').tobytes())
        self._shader.uniform("font_texture", 0)
        self._shader.uniform("char_size", (self._meta.character_width / self._meta.character_height, 1.0))
        self._vao.draw(self._shader, instances=len(self._string_data))
