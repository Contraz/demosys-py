from PIL import Image

from demosys.loaders.texture.base import BaseLoader
from demosys.opengl import TextureArray as Texture


class TextureArray(BaseLoader):
    name = 'array'

    def load(self):
        texture = Texture(self.path, **self.kwargs)
        image = Image.open(self.path)
        texture.set_image(image)
        return texture

