"""Shader Registry"""
from pathlib import Path
from typing import Union

import moderngl
from demosys.core.exceptions import ImproperlyConfigured
from demosys.core.shaderfiles.finders import get_finders
from demosys.opengl import ShaderError, ShaderProgram

from .base import BaseRegistry


class Shaders(BaseRegistry):
    """
    A registry for shaders requested by effects.
    Once all effects are initialized, we ask this class to load the shaders.
    """
    def __init__(self):
        super().__init__()
        self.shaders = {}

    @property
    def count(self):
        """
        :return: Number of shaders
        """
        return len(self.shaders)

    def get(self, path: Union[str, Path], create=False) -> ShaderProgram:
        """
        Get or create a shader object.
        This may return an empty object that will be filled during load
        based on the ``create`` parameter.

        :param path: Path to the shader (pathlib.Path instance)
        :param create: (bool) Create an empty shader object if it doesn't exist
        :return: Shader object
        """
        path = Path(path)

        shader = self.shaders.get(path)
        if create and not shader:
            shader = ShaderProgram(path)
            self.shaders[path] = shader
        return shader

    def load(self, reload=False):
        """
        Loads all the shaders using the configured finders.

        :param reload: (bool) Are we reloading the shaders?
        """
        print("Loading shaders:")
        for name, shader in self.shaders.items():
            self.load_shader(shader, name=name, reload=reload)

        self._on_loaded()

    def load_shader(self, shader, name=None, reload=False):
        """
        Loads a single shader adding it to the shader registry

        :param shader: The shader to load
        :param name: Unique name in the registry. Usually the path
        :param reload: (bool) Are we reloading the shader?
        """
        if name is None:
            name = shader.path

        finders = list(get_finders())

        for finder in finders:
            path = finder.find(name)
            if path:
                print(" - {}".format(path))
                with open(path, 'r') as fd:
                    shader.set_source(fd.read())

                try:
                    shader.prepare(reload=reload)
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
