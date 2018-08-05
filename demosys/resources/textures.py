"""Shader Registry"""
from pathlib import Path
from typing import Union

from demosys.conf import settings
from demosys.core.exceptions import ImproperlyConfigured
from demosys.core.texturefiles.finders import get_finders
from demosys.opengl import Texture2D, TextureArray
from demosys.utils.module_loading import import_string

from .base import BaseRegistry


class TextureMeta:

    def __init__(self, path, loader_cls, **kwargs):
        self.path = path
        self.loader_cls = loader_cls
        self.kwargs = kwargs


class Textures(BaseRegistry):
    """
    A registry for textures requested by effects.
    Once all effects are initialized, we ask this class to load the textures.
    """
    def __init__(self):
        super().__init__()
        self.loaders = [
            import_string(loader) for loader in settings.TEXTURE_LOADERS
        ]

    def get(self, path: Union[str, Path], loader='2d', **kwargs) -> Union[Texture2D, TextureArray]:
        """Compatibility with old resource system"""
        return self.load(path, loader=loader, **kwargs)

    def load(self, path: Union[str, Path], loader='2d', **kwargs) -> Union[Texture2D, TextureArray]:
        """
        Get or create a texture object.
        This may return an empty object that will be filled during loading stage

        :param path: Path to the texture
        :param cls: The texture class to instantiate
        :return: Texture object
        """
        path = Path(path)

        texture = self.file_map.get(path)
        if texture:
            return texture

        meta = self.load_deferred(path, loader, **kwargs)
        texture = self._load(meta)

        return texture

    def load_deferred(self, path: Union[str, Path], loader='2d', **kwargs) -> TextureMeta:
        meta = TextureMeta(path, self.get_loader(loader), **kwargs)

        self.file_map[path] = None
        self.file_meta[path] = meta

        return meta

    def _load(self, meta):
        """
        Loads all the textures using the configured finders.
        """
        found_path = self._find_last_of(meta.path, get_finders())

        if not found_path:
            raise ImproperlyConfigured("Cannot find texture {}".format(meta.path))

        print("Loading: {}".format(meta.path))
        texture = meta.loader_cls(found_path, **meta.kwargs).load()
        self.file_map[meta.path] = texture

        return texture

    def _destroy(self, obj):
        obj.release()

    def get_loader(self, name):
        for loader in self.loaders:
            if loader.name == name:
                return loader

        raise ValueError("Texture loader '{}' not registered. Available loaders: {}".format(
            name,
            [loader.name for loader in self.loaders]
        ))


textures = Textures()
