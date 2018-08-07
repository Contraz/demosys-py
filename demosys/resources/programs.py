"""Shader Registry"""
from demosys.conf import settings
from demosys.resources.base import BaseRegistry, ResourceDescription
from demosys.utils.module_loading import import_string


class ProgramDescription(ResourceDescription):
    require_label = True
    default_loader = 'single'

    def __init__(self, path=None, label=None, loader=None,
                 vertex_shader=None, geometry_shader=None, fragment_shader=None,
                 tess_control_shader=None, tess_evaluation_shader=None, **kwargs):
        kwargs.update({
            "path": path,
            "label": label,
            "loader": loader,
            "vertex_shader": vertex_shader,
            "geometry_shader": geometry_shader,
            "fragment_shader": fragment_shader,
            "tess_control_shader": tess_control_shader,
            "tess_evaluation_shader": tess_evaluation_shader,
        })
        super().__init__(kwargs)


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
