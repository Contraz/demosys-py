from demosys.resources import shaders
from .base import BaseText


class TextRenderer2D(BaseText):

    def __init__(self, area, size=0.1, text=""):
        """
        :param area: (x, y) Text area size (number of characters)
        :param size: Text size
        :param text: Initial text
        """
        super().__init__(text)
        self.area = area
        self.size = size
        self._text = text

        self.fbo = None
        self.vao = None
        self.shader = shaders.get('demosys/text/textwriter.glsl', create=True)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value

    def draw(self):
        pass
