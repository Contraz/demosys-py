"""Shader Registry"""
from demosys.conf import settings
from demosys.resources.base import BaseRegistry
from demosys.utils.module_loading import import_string


class Textures(BaseRegistry):
    """
    A registry for textures requested by effects.
    Once all effects are initialized, we ask this class to load the textures.
    """
    def __init__(self):
        super().__init__()
        self._loaders = [
            import_string(loader) for loader in settings.TEXTURE_LOADERS
        ]


textures = Textures()
