from PIL import Image

from demosys.loaders.texture.base import BaseLoader
from demosys.opengl import Texture2D as Texture


class Texture2D(BaseLoader):
    name = '2d'

    def load(self):
        texture = Texture(path=self.path, **self.kwargs)
        image = Image.open(self.path)
        texture.set_image(image)
        return texture
