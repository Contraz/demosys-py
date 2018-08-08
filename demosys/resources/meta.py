from demosys.resources.base import ResourceDescription


class DataDescription(ResourceDescription):
    """Describes data file to load"""
    require_label = True
    default_loader = 'binary'
    resource_type = 'data'

    def __init__(self, path=None, label=None, loader=None, **kwargs):
        kwargs.update({
            "path": path,
            "label": label,
            "loader": loader,
        })
        super().__init__(**kwargs)


class ProgramDescription(ResourceDescription):
    """Describes a program to load"""
    require_label = True
    default_loader = 'single'
    resource_type = 'programs'

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
        super().__init__(**kwargs)


class SceneDescription(ResourceDescription):
    """Describes a scene to load"""
    require_label = True
    default_loader = None
    resource_type = 'scenes'

    def __init__(self, path=None, label=None, **kwargs):
        kwargs.update({
            "path": path,
            "label": label,
        })
        super().__init__(**kwargs)


class TextureDescription(ResourceDescription):
    """Describes a texture to load"""
    require_label = True
    default_loader = '2d'
    resource_type = 'textures'

    def __init__(self, path=None, label=None, loader=None, **kwargs):
        kwargs.update({
            "path": path,
            "label": label,
            "loader": loader,
        })
        super().__init__(**kwargs)