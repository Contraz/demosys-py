from typing import Any, Type

from pyrr import Matrix33, Matrix44, Vector3, matrix44
from rocket.tracks import Track

import moderngl
from demosys import resources
from demosys.context.base import Window  # noqa
from demosys.scene import camera  # noqa
from demosys.scene import Scene


class Effect:
    """
    Effect base class.

    The following attributes are injected by demosys before initialization:

    * ``window`` (demosys.context.Context): Window
    * ``ctx`` (moderngl.Context): The moderngl context
    * ``sys_camera`` (demosys.scene.camera.Camera): The system camera responding to inputs
    """
    # By default effects are runnable with ``runeffect``
    runnable = True

    # Full python path to the effect (set per instance)
    _name = ""
    _label = ""

    # Window properties set by controller on initialization (class vars)
    _window = None  # type: Window
    _project = None  # type: demosys.project.base.BaseProject

    _ctx = None  # type: moderngl.Context
    _sys_camera = None  # type: camera.SystemCamera

    def post_load(self):
        """
        Called when all effects are initialized before effects start running.
        """
        pass

    @property
    def name(self) -> str:
        """Full python path to the effect"""
        return self._name

    @property
    def label(self) -> str:
        """Full python path to the effect"""
        return self._label

    @property
    def window(self) -> Window:
        return self._window

    @property
    def ctx(self) -> moderngl.Context:
        """ModernGL context"""
        return self._ctx

    @property
    def sys_camera(self) -> camera.SystemCamera:
        """The system camera responding to input"""
        return self._sys_camera

    # Methods to override
    def draw(self, time, frametime, target):
        """
        Draw function called by the system every frame when the effect is active.
        You are supposed to override this method.

        :param time: The current time in seconds (float)
        :param frametime: The time the previous frame used to render in seconds (float)
        :param target: The target FBO for the effect
        """
        raise NotImplementedError("draw() is not implemented")

    # Methods for getting resources

    def get_program(self, label) -> moderngl.Program:
        """
        Get a program by its label

        :param label: The label for the program
        :return: moderngl.Program instance
        """
        return self._project.get_program(label)

    def get_texture(self, label) -> moderngl.Texture:
        """
        Get a texture by its label

        :param label: Label for the texture
        :return: The moderngl texture instance
        """
        return self._project.get_texture(label)

    def get_track(self, name) -> Track:
        """
        Get or create a rocket track. This only makes sense when using rocket timers.
        If the resource is not loaded yet, an empty track object
        is returned that will be populated later.

        :param name: The rocket track name
        :param local: Auto-prepend the effect package name to the path
        :return: Track object
        """
        return resources.tracks.get(name)

    def get_scene(self, label) -> Scene:
        """
        Get a scene by its label

        :param label: The label for the scene
        :return: Scene object
        """
        return self._project.get_scene(label)

    def get_data(self, label) -> Any:
        """
        Get a data file by its label

        :param label: Label for the data file
        :return: Contents of the data file
        """
        return self._project.get_data(label)

    def get_effect(self, label) -> 'Effect':
        """
        Get an effect instance by label

        :param label: Label for the data file
        :return: The requested effect instance
        """
        return self._project.get_effect(label)

    def get_effect_class(self, effect_name, package_name=None) -> Type['Effect']:
        """
        Get an effect class.

        :param effect_name: Name of the effect class
        :param package_name: (optional) The package this effect belongs to
        """
        return self._project.get_effect_class(effect_name, package_name=package_name)

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
            ratio or self.window.aspect_ratio,
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
