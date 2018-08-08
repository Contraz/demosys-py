"""Shader Registry"""
from demosys.conf import settings
from demosys.resources.base import BaseRegistry
from demosys.utils.module_loading import import_string


class Programs(BaseRegistry):
    """
    A registry for shaders requested by effects.
    Once all effects are initialized, we ask this class to load the shaders.
    """
    def __init__(self):
        super().__init__()
        self._loaders = [
            import_string(loader) for loader in settings.PROGRAM_LOADERS
        ]


programs = Programs()
