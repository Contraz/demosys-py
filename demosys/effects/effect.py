from demosys import resources
from pyrr import matrix44, Matrix33, Vector3


def bind_target(func):
    """Decorator auto binding and releasing the incoming FBO"""
    def func_wrapper(*args, **kwargs):
        args[2].bind()
        func(*args, **kwargs)
        args[2].release()
    return func_wrapper


class Effect:
    # Window properties set by controller on initialization
    name = ""
    window_width = 0
    window_height = 0
    window_aspect = 0
    sys_camera = None

    def __init__(self, name=name):
        self.name = name

    # Methods to override
    def draw(self, time, target):
        raise NotImplemented

    # Utility Stuff
    def get_shader(self, path):
        return resources.shaders.get(path, create=True)

    def get_texture(self, path):
        return resources.textures.get(path, create=True)

    def create_projection(self, fov=75.0, near=1.0, far=100.0, ratio=None):
        return matrix44.create_perspective_projection_matrix(
            fov,
            ratio or self.window_aspect,
            near,
            far,
        )

    def create_transformation(self, rotation=None, translation=None):
        """Convenient transformation method doing rotations and translation"""
        mat = None
        if rotation:
            x = matrix44.create_from_x_rotation(rotation[0])
            y = matrix44.create_from_y_rotation(rotation[1])
            z = matrix44.create_from_z_rotation(rotation[2])
            mat = matrix44.multiply(x, y)
            mat = matrix44.multiply(mat, z)

        if translation:
            trans = matrix44.create_from_translation(Vector3(translation))
            if mat is None:
                mat = trans
            else:
                mat = matrix44.multiply(mat, trans)

        return mat

    def create_normal_matrix(self, modelview):
        """Convert to mat3 and return inverse transpose"""
        normal_m = Matrix33.from_matrix44(modelview)
        normal_m = normal_m.inverse
        normal_m = normal_m.transpose()
        return normal_m
