"""Shader Registry"""
from demosys.opengl import Texture
from demosys.core.texturefiles.finders import get_finders
from demosys.core.exceptions import ImproperlyConfigured
from PIL import Image


class Textures:
    def __init__(self):
        self.textures = {}

    @property
    def count(self):
        return len(self.textures)

    def get(self, path, create=False):
        texture = self.textures.get(path)
        if create and not texture:
            texture = Texture.from_image(path)
            self.textures[path] = texture
        return texture

    def load(self):
        finders = list(get_finders())
        print("Loading textures:")
        for name, texture in self.textures.items():
            for finder in finders:
                path = finder.find(name)
                if path:
                    print(" - {}".format(path))
                    image = Image.open(path)
                    texture.set_image(image)
                    break
            else:
                raise ImproperlyConfigured("Cannot find texture {name}")


textures = Textures()
