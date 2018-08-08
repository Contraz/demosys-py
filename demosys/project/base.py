from demosys import context
from demosys import resources
from demosys.effects.registry import effects
from demosys.effects import Effect


class BaseProject:
    """The Project"""

    def __init__(self):
        self.effects = {}
        self.programs = {}
        self.textures = {}
        self.scenes = {}
        self.data = {}

    def create_resources(self):
        # Just return the external list
        return self._get_external_resources()

    def create_effects(self):
        raise NotImplementedError()

    def load(self):
        # Throw each resource into their respective pools
        for meta in self.create_resources():
            resources.add(meta)

        for meta, resource in resources.textures.load_pool():
            self.textures[meta.label] = resource

        for meta, resource in resources.programs.load_pool():
            self.programs[meta.label] = resource

        for meta, resource in resources.scenes.load_pool():
            self.scenes[meta.label] = resource

        for meta, resource in resources.data.load_pool():
            self.data[meta.label] = resource

        self.create_effects()
        self._post_load()

    def _post_load(self):
        for _, effect in self.effects.items():
            effect.post_load()

    def _get_external_resources(self):
        """Get resources from effect modules or injected elsewhere"""
        # We need to get this from the effects registry
        return []

    def create_effect(self, label, python_path: str, **kwargs):
        """Create an effect instance"""
        effect_cls = effects.get_effect_cls(python_path)
        self.effects[label] = effect_cls(**kwargs)

    def get_effect(self, label):
        return self.effects[label]

    def get_scene(self, label):
        return self.scenes[label]

    def get_program(self, label):
        return self.programs[label]

    def get_texture(self, label):
        return self.textures[label]

    def get_data(self, label):
        return self.data[label]

    @property
    def ctx(self):
        return context.ctx()
