from demosys import context
from demosys import resources
from demosys.effects.registry import effects
from demosys.effects import Effect
from demosys.conf import settings


class BaseProject:
    """The Project"""

    def __init__(self):
        self._effects = {}
        self._programs = {}
        self._textures = {}
        self._scenes = {}
        self._data = {}

    def create_effect_classes(self):
        """Create effect classes in the registry"""
        effects.polulate(settings.EFFECTS)

    def create_external_resources(self):
        """
        Create resources defined externally such as resource modules in effect packages.

        :returns: List of resource descriptions to load
        """
        return effects.get_effect_resources()

    def create_resources(self):
        """
        Create resources for the project

        :returns: List of resource descriptions to load
        """
        raise NotImplementedError()

    def create_effect_instances(self):
        """
        Create instances of effects
        """
        raise NotImplementedError()

    def create_effect(self, label, class_name, package_name=None, **kwargs):
        """Create an effect instance"""
        effect_cls = effects.find_effect_class(class_name, package_name=package_name)
        effect = effect_cls(**kwargs)

        if label in self._effects:
            raise ValueError("An effect with label '{}' already exists".format(label))

        self._effects[label] = effect

        return effect

    def post_load(self):
        """
        Actions after loading is complete
        """
        for _, effect in self._effects.items():
            effect.post_load()

    def load(self):
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
        if not meta_list:
            return

        for meta in meta_list:
            getattr(resources, meta.resource_type).add(meta)

    def get_effect(self, label):
        return self._effects[label]

    def get_scene(self, label):
        return self._scenes[label]

    def get_program(self, label):
        return self._programs[label]

    def get_texture(self, label):
        return self._textures[label]

    def get_data(self, label):
        return self._data[label]

    @property
    def ctx(self):
        return context.ctx()
