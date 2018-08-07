"""Shader Registry"""
from demosys.conf import settings
from demosys.resources.base import BaseRegistry, ResourceDescription
from demosys.utils.module_loading import import_string


class TextureDescription(ResourceDescription):
    require_label = True
    default_loader = '2d'

    def __init__(self, path=None, label=None, loader=None, **kwargs):
        kwargs.update({
            "path": path,
            "label": label,
            "loader": loader,
        })
        super().__init__(kwargs)


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


textures = Textures()
