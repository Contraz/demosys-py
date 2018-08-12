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

    def __init__(self, path=None, label=None, loader=None, reloadable=False,
                 vertex_shader=None, geometry_shader=None, fragment_shader=None,
                 tess_control_shader=None, tess_evaluation_shader=None, **kwargs):
        kwargs.update({
            "path": path,
            "label": label,
            "loader": loader,
            "reloadable": reloadable,
            "vertex_shader": vertex_shader,
            "geometry_shader": geometry_shader,
            "fragment_shader": fragment_shader,
            "tess_control_shader": tess_control_shader,
            "tess_evaluation_shader": tess_evaluation_shader,
        })
        super().__init__(**kwargs)

    @property
    def reloadable(self):
        return self.kwargs.get('reloadable')

    @reloadable.setter
    def reloadable(self, value):
        self.kwargs['reloadable'] = value


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

    def __init__(self, path=None, label=None, loader=None, flip=True, mipmap=True, image=None, **kwargs):
        kwargs.update({
            "path": path,
            "label": label,
            "loader": loader,
            "flip": flip,
            "image": image,
            "mipmap": mipmap,
        })
        super().__init__(**kwargs)

    @property
    def flip(self):
        return self.kwargs.get('flip')

    @property
    def image(self):
        return self.kwargs.get('image')

    @property
    def mipmap(self):
        return self.kwargs.get('mipmap')
