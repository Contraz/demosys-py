"""Shader Registry"""
from pathlib import Path
from typing import Union

import moderngl
from demosys.core.exceptions import ImproperlyConfigured
from demosys.core.shaderfiles.finders import get_finders
from demosys.opengl import ShaderError, ShaderProgram

from .base import BaseRegistry


class ShaderMeta:

    def __init__(self, path, **kwargs):
        self.path = path
        self.kwargs = kwargs


class Shaders(BaseRegistry):
    """
    A registry for shaders requested by effects.
    Once all effects are initialized, we ask this class to load the shaders.
    """
    def __init__(self):
        super().__init__()

    def get(self, path: Union[str, Path], **kwargs) -> ShaderProgram:
        """Compatibility method with the old resource system"""
        return self.load(path, **kwargs)

    def load(self, path: Union[str, Path], **kwargs) -> ShaderProgram:
        """
        load shader program or return an exiting program.

        :param path: Path to the shader (pathlib.Path instance)
        :return: Shader object
        """
        path = Path(path)

        shader = self.file_map.get(path)
        if shader:
            return shader

        meta = self.load_deferred(path, **kwargs)
        shader = self._load(meta)

        return shader

    def load_deferred(self, path: Union[str, Path], **kwargs) -> ShaderMeta:
        meta = ShaderMeta(path, **kwargs)

        self.file_map[path] = None
        self.file_meta[path] = meta

        return meta

    def _load(self, meta, reload=False):
        found_path = self._find_last_of(meta.path, list(get_finders()))

        if not found_path:
            raise ImproperlyConfigured("Cannot find shader {}".format(meta.path))

        print("Loading: {}".format(meta.path))
        if reload:
            shader = self.file_map[meta.path]
        else:
            shader = ShaderProgram(meta.path)

        with open(found_path, 'r') as fd:
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

        self.file_map[meta.path] = shader

        return shader

    def _destroy(self, obj):
        obj.release()

    def reload(self):
        """
        Reloads all shaders
        """
        for path, meta in self.file_meta.items():
            print(path, meta)
            self._load(meta, reload=True)


shaders = Shaders()
