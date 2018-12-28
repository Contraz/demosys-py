from typing import Any, List, Type, Union

import moderngl
from demosys import context, resources
from demosys.effects import Effect
from demosys.effects.registry import effects
from demosys.resources.meta import ResourceDescription
from demosys.scene import Scene


class BaseProject:
    """
    The base project class we extend when creating a project configuration

    The minimal implementation::

        from demosys.project.base import BaseProject
        from demosys.resources.meta import ProgramDescription, TextureDescription

        class Project(BaseProject):
            # The effect packages to import using full python path
            effect_packages = [
                'myproject.efect_package1',
                'myproject.efect_package2',
                'myproject.efect_package2',
            ]
            # Resource description for global project resources (not loaded by effect packages)
            resources = [
                ProgramDescription(label='cube_textured', path="cube_textured.glsl'),
                TextureDescription(label='wood', path="wood.png', mipmap=True),
            ]

            def create_resources(self):
                # Override the method adding additional resources

                # Create some shared fbo
                size = (256, 256)
                self.shared_framebuffer = self.ctx.framebuffer(
                    color_attachments=self.ctx.texture(size, 4),
                    depth_attachement=self.ctx.depth_texture(size)
                )

                return self.resources

            def create_effect_instances(self):
                # Create and register instances of an effect class we loaded from the effect packages
                self.create_effect('cube1', 'CubeEffect')

                # Using full path to class
                self.create_effect('cube2', 'myproject.efect_package1.CubeEffect')

                # Passing variables to initializer
                self.create_effect('cube3', 'CubeEffect', texture=self.get_texture('wood'))

                # Assign resources manually
                cube = self.create_effect('cube1', 'CubeEffect')
                cube.program = self.get_program('cube_textured')
                cube.texture = self.get_texture('wood')
                cube.fbo = self.shared_framebuffer

    These effects instances can then be obtained by the configured timeline class deciding
    when they should be rendered.
    """
    effect_packages = []  #: The effect packages to load
    resources = []  #: Global project resource descriptions

    def __init__(self):
        self._effects = {}
        self._programs = {}
        self._textures = {}
        self._scenes = {}
        self._data = {}

    def create_effect_classes(self):
        """
        Registers effect packages defined in ``effect_packages``.
        """
        effects.polulate(self.effect_packages)

    def create_external_resources(self) -> List[ResourceDescription]:
        """
        Fetches all resource descriptions defined in effect packages.

        Returns:
            List of resource descriptions to load
        """
        return effects.get_effect_resources()

    def create_resources(self) -> List[ResourceDescription]:
        """
        Create resources for the project.
        Simply returns the ``resources`` list and can be implemented to
        modify what a resource list is programmatically.

        Returns:
            List of resource descriptions to load
        """
        return self.resources

    def create_effect_instances(self):
        """
        Create instances of effects.
        Must be implemented or ``NotImplementedError`` is raised.
        """
        raise NotImplementedError()

    def create_effect(self, label: str, name: str, *args, **kwargs) -> Effect:
        """
        Create an effect instance adding it to the internal effects dictionary using the label as key.

        Args:
            label (str): The unique label for the effect instance
            name (str): Name or full python path to the effect class we want to instantiate
            args: Positional arguments to the effect initializer
            kwargs: Keyword arguments to the effect initializer

        Returns:
            The newly created Effect instance
        """
        effect_cls = effects.find_effect_class(name)
        effect = effect_cls(*args, **kwargs)
        effect._label = label

        if label in self._effects:
            raise ValueError("An effect with label '{}' already exists".format(label))

        self._effects[label] = effect

        return effect

    def post_load(self):
        """
        Called after resources are loaded before effects starts rendering.
        It simply iterates each effect instance calling their ``post_load`` methods.
        """
        for _, effect in self._effects.items():
            effect.post_load()

    def load(self):
        """
        Loads this project instance
        """
        self.create_effect_classes()

        self._add_resource_descriptions_to_pools(self.create_external_resources())
        self._add_resource_descriptions_to_pools(self.create_resources())

        for meta, resource in resources.textures.load_pool():
            self._textures[meta.label] = resource

        for meta, resource in resources.programs.load_pool():
            self._programs[meta.label] = resource

        for meta, resource in resources.scenes.load_pool():
            self._scenes[meta.label] = resource

        for meta, resource in resources.data.load_pool():
            self._data[meta.label] = resource

        self.create_effect_instances()
        self.post_load()

    def _add_resource_descriptions_to_pools(self, meta_list):
        """
        Takes a list of resource descriptions adding them
        to the resource pool they belong to scheduling them for loading.
        """
        if not meta_list:
            return

        for meta in meta_list:
            getattr(resources, meta.resource_type).add(meta)

    def reload_programs(self):
        """
        Reload all shader programs with the reloadable flag set
        """
        print("Reloading programs:")
        for name, program in self._programs.items():
            if getattr(program, 'program', None):
                print(" - {}".format(program.meta.label))
                program.program = resources.programs.load(program.meta)

    def get_effect(self, label: str) -> Effect:
        """
        Get an effect instance by label

        Args:
            label (str): The label for the effect instance

        Returns:
            Effect class instance
        """
        return self._get_resource(label, self._effects, "effect")

    def get_effect_class(self, class_name, package_name=None) -> Type[Effect]:
        """
        Get an effect class from the effect registry.

        Args:
            class_name (str): The exact class name of the effect

        Keyword Args:
            package_name (str): The python path to the effect package the effect name is located.
                                This is optional and can be used to avoid issue with class name collisions.

        Returns:
            Effect class
        """
        if package_name:
            return effects.find_effect_class("{}.{}".format(package_name, class_name))

        return effects.find_effect_class(class_name)

    def get_scene(self, label: str) -> Scene:
        """
        Gets a scene by label

        Args:
            label (str): The label for the scene to fetch

        Returns:
            Scene instance
        """
        return self._get_resource(label, self._scenes, "scene")

    def get_program(self, label: str) -> moderngl.Program:
        return self._get_resource(label, self._programs, "program")

    def get_texture(self, label: str) -> Union[moderngl.Texture, moderngl.TextureArray,
                                               moderngl.Texture3D, moderngl.TextureCube]:
        """
        Get a texture by label

        Args:
            label (str): The label for the texture to fetch

        Returns:
            Texture instance
        """
        return self._get_resource(label, self._textures, "texture")

    def get_data(self, label: str) -> Any:
        """
        Get a data resource by label

        Args:
            label (str): The labvel for the data resource to fetch

        Returns:
            The requeted data object
        """
        return self._get_resource(label, self._data, "data")

    def _get_resource(self, label: str, source: dict, resource_type: str):
        """
        Generic resoure fetcher handling errors.

        Args:
            label (str): The label to fetch
            source (dict): The dictionary to look up the label
            resource_type str: The display name of the resource type (used in errors)
        """
        try:
            return source[label]
        except KeyError:
            raise ValueError("Cannot find {0} with label '{1}'.\nExisting {0} labels: {2}".format(
                resource_type, label, list(source.keys())))

    def get_runnable_effects(self) -> List[Effect]:
        """
        Returns all runnable effects in the project.

        :return: List of all runnable effects
        """
        return [effect for name, effect in self._effects.items() if effect.runnable]

    @property
    def ctx(self) -> moderngl.Context:
        """The MondernGL context"""
        return context.ctx()
