from typing import Any, Type, Union

from pyrr import Matrix33, Matrix44, Vector3, matrix44
from rocket.tracks import Track

import moderngl
from demosys import resources
from demosys.context.base import BaseWindow  # noqa
from demosys.scene import camera  # noqa
from demosys.scene import Scene


class Effect:
    """
    The base Effect base class that should be extended when making an effect.

    The typical example::

        import moderngl
        from demosys.effects import Effect
        from demosys import geometry

        class MyEffect(Effect):
            def __init__(self):
                # Initalization happens after resources are loaded
                self.program = self.get_program("my_program_label")
                self.fullscreen_quad = geometry.quad_fs()

            def post_load(self):
                # Initialization after all effects are initialized

            def draw(self, time, frametime, target):
                # Render a colored fullscreen quad
                self.ctx.enable_only(moderngl.DEPTH_TEST)
                self.program["color"].value = (1.0, 1.0, 1.0, 1.0)
                self.fullscreen_quad.render(self.program)
    """
    #: The runnable status of the effect instance.
    #: A runnable effect should be able to run with the ``runeffect`` command
    #: or run in a project
    runnable = True

    # Full python path to the effect (set per instance)
    _name = ""
    _label = ""

    # Window properties set by controller on initialization (class vars)
    _window = None  # type: BaseWindow
    _project = None  # type: 'demosys.project.base.BaseProject'

    _ctx = None  # type: moderngl.Context
    _sys_camera = None  # type: camera.SystemCamera

    def __init__(self, *args, **kwargs):
        """
        Implement the initialize when extending the class.
        This method is responsible for fetching or creating resources
        and doing genereal initalization of the effect.

        The effect initializer is called when all resources are loaded
        (with the exception of resources you manually load in the
        the initializer).

        If your effect requires arguments during initialiation you
        are free to add positional and keyword arguments.

        You **do not** have to call the superclass initializer though ``super()``

        Example::

            def __init__(self):
                # Fetch reference to resource by their label
                self.program = self.get_program('simple_textured')
                self.texture = self.get_texture('bricks')
                # .. create a cube etc ..
        """
        pass

    def post_load(self):
        """
        Called after all effects are initialized before drawing starts.
        Some initialization may be neccessary to do here such as
        interaction with other effects.

        This method does nothing unless implemented.
        """
        pass

    @property
    def name(self) -> str:
        """Full python path to the effect"""
        return self._name

    @property
    def label(self) -> str:
        """The label assigned to this effect instance"""
        return self._label

    @property
    def window(self) -> BaseWindow:
        """The :py:class:`Window`"""
        return self._window

    @property
    def ctx(self) -> moderngl.Context:
        """The ModernGL context"""
        return self._ctx

    @property
    def sys_camera(self) -> camera.SystemCamera:
        """The system camera responding to input"""
        return self._sys_camera

    # Methods to override
    def draw(self, time: float, frametime: float, target: moderngl.Framebuffer):
        """
        Draw function called by the system every frame when the effect is active.
        This method raises ``NotImplementedError`` unless implemented.

        Args:
            time (float): The current time in seconds.
            frametime (float): The time the previous frame used to render in seconds.
            target (``moderngl.Framebuffer``): The target FBO for the effect.
        """
        raise NotImplementedError("draw() is not implemented")

    # Methods for getting resources

    def get_program(self, label: str) -> moderngl.Program:
        """
        Get a program by its label

        Args:
            label (str): The label for the program

        Returns: py:class:`moderngl.Program` instance
        """
        return self._project.get_program(label)

    def get_texture(self, label: str) -> Union[moderngl.Texture, moderngl.TextureArray,
                                               moderngl.Texture3D, moderngl.TextureCube]:
        """
        Get a texture by its label

        Args:
            label (str): The Label for the texture

        Returns:
            The py:class:`moderngl.Texture` instance
        """
        return self._project.get_texture(label)

    def get_track(self, name: str) -> Track:
        """
        Gets or creates a rocket track.
        Only avaiable when using a Rocket timer.

        Args:
            name (str): The rocket track name

        Returns:
            The :py:class:`rocket.Track` instance
        """
        return resources.tracks.get(name)

    def get_scene(self, label: str) -> Scene:
        """
        Get a scene by its label

        Args:
            label (str): The label for the scene

        Returns: The :py:class:`Scene` instance
        """
        return self._project.get_scene(label)

    def get_data(self, label: str) -> Any:
        """
        Get a data instance by its label

        Args:
            label (str): Label for the data instance

        Returns:
            Contents of the data file
        """
        return self._project.get_data(label)

    def get_effect(self, label: str) -> 'Effect':
        """
        Get an effect instance by label.

        Args:
            label (str): Label for the data file

        Returns: The :py:class:`Effect` instance
        """
        return self._project.get_effect(label)

    def get_effect_class(self, effect_name: str, package_name: str = None) -> Type['Effect']:
        """
        Get an effect class by the class name

        Args:
            effect_name (str): Name of the effect class

        Keyword Args:
            package_name (str): The package the effect belongs to. This is optional and only
                                needed when effect class names are not unique.

        Returns:
            :py:class:`Effect` class
        """
        return self._project.get_effect_class(effect_name, package_name=package_name)

    # Utility methods for matrices

    def create_projection(self, fov: float = 75.0, near: float = 1.0, far: float = 100.0, aspect_ratio: float = None):
        """
        Create a projection matrix with the following parameters.
        When ``aspect_ratio`` is not provided the configured aspect
        ratio for the window will be used.

        Args:
            fov (float): Field of view (float)
            near (float): Camera near value
            far (float): Camrea far value

        Keyword Args:
            aspect_ratio (float): Aspect ratio of the viewport

        Returns:
            The projection matrix as a float32 :py:class:`numpy.array`
        """
        return matrix44.create_perspective_projection_matrix(
            fov,
            aspect_ratio or self.window.aspect_ratio,
            near,
            far,
            dtype='f4',
        )

    def create_transformation(self, rotation=None, translation=None):
        """
        Creates a transformation matrix woth rotations and translation.

        Args:
            rotation: 3 component vector as a list, tuple, or :py:class:`pyrr.Vector3`
            translation: 3 component vector as a list, tuple, or :py:class:`pyrr.Vector3`

        Returns:
            A 4x4 matrix as a :py:class:`numpy.array`
        """
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
        Creates a normal matrix from modelview matrix

        Args:
            modelview: The modelview matrix

        Returns:
            A 3x3 Normal matrix as a :py:class:`numpy.array`
        """
        normal_m = Matrix33.from_matrix44(modelview)
        normal_m = normal_m.inverse
        normal_m = normal_m.transpose()
        return normal_m
