"""Shader Registry"""
import moderngl

from demosys.opengl import (ShaderProgram, ShaderError)
from demosys.core.shaderfiles.finders import get_finders
from demosys.core.exceptions import ImproperlyConfigured


class Shaders:
    """
    A registry for shaders requested by effects.
    Once all effects are initialized, we ask this class to load the shaders.
    """
    def __init__(self):
        self.shaders = {}

    @property
    def count(self):
        """
        :return: Number of shaders
        """
        return len(self.shaders)

    def get(self, path, create=False):
        """
        Get or create a shader object.
        This may return an empty object that will be filled during load
        based on the ``create`` parameter.

        :param path: Path to the shader
        :param create: (bool) Create an empty shader object if it doesn't exist
        :return: Shader object
        """
        shader = self.shaders.get(path)
        if create and not shader:
            shader = ShaderProgram(path)
            self.shaders[path] = shader
        return shader

    def load(self, reload=False):
        """
        Loads all the shaders using the configured finders.
        """
        finders = list(get_finders())
        print("Loading shaders:")
        for name, shader in self.shaders.items():
            for finder in finders:
                path = finder.find(name)
                if path:
                    print(" - {}".format(path))
                    with open(path, 'r') as fd:
                        shader.set_source(fd.read())

                    try:
                        shader.prepare()
                    except (ShaderError, moderngl.Error) as err:
                        print("ShaderError: ", err)
                        if not reload:
                            raise
                    except Exception as err:
                        print(err)
                        raise

                    break
            else:
                raise ImproperlyConfigured("Cannot find shader {}".format(name))

    def reload(self):
        """
        Reloads all shaders
        """
        self.load(reload=True)


shaders = Shaders()
