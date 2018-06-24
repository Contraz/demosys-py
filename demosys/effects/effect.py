import os
from demosys import resources
from pyrr import matrix44, Matrix33, Matrix44, Vector3


def bind_target(func):
    """
    Decorator auto binding and releasing the incoming FBO in ``draw()``.

    literal blocks::

       @bind_target
        def draw(...):
            # draw stuff
    """
    def func_wrapper(*args, **kwargs):
        args[3].bind()
        func(*args, **kwargs)
        args[3].release()
    return func_wrapper


def local_path(func):
    """
    Decorator modifying the `path` parameter depending
    on the `local` parameter.
    If `local` is `True` we prepend the current effect name to the path.
    """
    def local_wrapper(*args, **kwargs):
        use_local = kwargs.get('local')

        # If use_local is True prepend the package name to the path
        if use_local is True:
                path = args[1]
                path = os.path.join(args[0].effect_name, path)

                # Replace path and rebuild tuple
                args = list(args)
                args[1] = path
                args = tuple(args)

        return func(*args, **kwargs)
    return local_wrapper


class Effect:
    """Effect base class.

    The following attributes are injected by demosys before initialization:

    * window_width (int): Window width in pixels
    * window_height (int): Window height in pixels
    * window_aspect (float): Aspect ratio of the resolution
    * sys_camera (demosys.scene.camera.Camera): The system camera responding to inputs
    """
    # Full python path to the effect (set per instance)
    name = ""

    # Window properties set by controller on initialization (class vars)
    window_width = 0
    window_height = 0
    window_aspect = 0

    # ModernGL context
    ctx = None

    # System camera
    sys_camera = None

    @property
    def effect_name(self):
        """Returns the package name for the effect"""
        return self.name.split('.')[-1]

    # Methods to override
    def draw(self, time, frametime, target):
        """Draw function called by the system every frame.

        :param time: The current time in seconds (float)
        :param frametime: The number of milliseconds the frame is expected to take
        :param target: The target FBO for the effect
        """
        raise NotImplementedError("draw() is not implemented")

    # Methods for getting resources

    @local_path
    def get_shader(self, path, local=False):
        """
        Get a shader or schedule the shader for loading.
        If the resource is not loaded yet, an empty shader object
        is returned that will be populated later.

        :param path: Path to the shader in the virtual shader directory
        :param local: Auto-prepend the local effect path
        :return: Shader object
        """
        return resources.shaders.get(path, create=True)

    @local_path
    def get_texture(self, path, local=False, **kwargs):
        """
        Get a shader or schedule the texture for loading.
        If the resource is not loaded yet, an empty texture object
        is returned that will be populated later.

        :param path: Path to the texture in the virtual texture directory
        :param local: Auto-prepend the local effect path
        :return: Texture object
        """
        return resources.textures.get(path, create=True, **kwargs)

    @local_path
    def get_track(self, name, local=False):
        """
        Get or create a rocket track. This only makes sense when using rocket timers.
        If the resource is not loaded yet, an empty track object
        is returned that will be populated later.

        :param name: The rocket track name
        :param local: Auto-prepend the local effect path
        :return: Track object
        """
        return resources.tracks.get(name)

    @local_path
    def get_scene(self, path, local=False, **kwargs):
        """
        Get or create a scene.
        :param path: Path to the scene
        :param local: Auto-prepend the local effect path
        :param kwargs: Generic paramters passed to scene loaders
        :return: Scene object
        """
        return resources.scenes.get(path, create=True, **kwargs)

    # Utility methods for matrices

    def create_projection(self, fov=75.0, near=1.0, far=100.0, ratio=None):
        """
        Create a projection matrix with the following parameters.

        :param fov: Field of view (float)
        :param near: Camera near value
        :param far: Camrea far value
        :param ratio: Aspect ratio of the window
        :return: The projection matrix
        """
        return matrix44.create_perspective_projection_matrix(
            fov,
            ratio or self.window_aspect,
            near,
            far,
        )

    def create_transformation(self, rotation=None, translation=None):
        """Convenient transformation method doing rotations and translation"""
        mat = None
        if rotation is not None:
            mat = Matrix44.from_eulers(Vector3(rotation))

        if translation is not None:
            trans = matrix44.create_from_translation(Vector3(translation))
            if mat is None:
                mat = trans
            else:
                mat = matrix44.multiply(mat, trans)

        return mat

    def create_normal_matrix(self, modelview):
        """
        Convert to mat3 and return inverse transpose.
        These are normally needed when dealing with normals in shaders.

        :param modelview: The modelview matrix
        :return: Normal matrix
        """
        normal_m = Matrix33.from_matrix44(modelview)
        normal_m = normal_m.inverse
        normal_m = normal_m.transpose()
        return normal_m
