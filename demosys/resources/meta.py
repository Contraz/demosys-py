from demosys.resources.base import ResourceDescription


class DataDescription(ResourceDescription):
    """Describes data file to load"""
    require_label = True
    default_loader = 'binary'

    def __init__(self, path=None, label=None, loader=None, **kwargs):
        kwargs.update({
            "path": path,
            "label": label,
            "loader": loader,
        })
        super().__init__(kwargs)


class ProgramDescription(ResourceDescription):
    """Describes a program to load"""
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


class SceneDescription(ResourceDescription):
    """Describes a scene to load"""
    require_label = True
    default_loader = None

    def __init__(self, path=None, label=None, mesh_programs=None, **kwargs):
        kwargs.update({
            "path": path,
            "label": label,
            "mesh_programs": mesh_programs,
        })
        super().__init__(kwargs)


class TextureDescription(ResourceDescription):
    """Describes a texture to load"""
    require_label = True
    default_loader = '2d'

    def __init__(self, path=None, label=None, loader=None, **kwargs):
        kwargs.update({
            "path": path,
            "label": label,
            "loader": loader,
        })
        super().__init__(kwargs)
