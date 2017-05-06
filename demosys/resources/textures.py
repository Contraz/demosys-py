"""Shader Registry"""
from demosys.opengl import Texture
from demosys.core.texturefiles.finders import get_finders
from demosys.core.exceptions import ImproperlyConfigured
from PIL import Image


class Textures:
    """
    A registry for textures requested by effects.
    Once all effects are initialized, we ask this class to load the textures.
    """
    def __init__(self):
        self.textures = {}

    @property
    def count(self):
        """
        :return: Number of textures
        """
        return len(self.textures)

    def get(self, path, create=False, **kwargs):
        """
        Get or create a texture object.
        This may return an empty object that will be filled during load
        based on the ``create`` parameter.

        :param path: Path to the texture
        :param create: (bool) Create an empty texture object if it doesn't exist
        :return: Texture object
        """
        texture = self.textures.get(path)
        if create and not texture:
            texture = Texture.from_image(path, **kwargs)
            self.textures[path] = texture
        return texture

    def load(self):
        """
        Loads all the textures using the configured finders.
        """
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
