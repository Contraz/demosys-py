from demosys import context
from demosys import resources


class Project:
    """The Project"""

    def __init__(self):
        self.effects = {}
        self.programs = {}
        self.textures = {}
        self.scenes = {}
        self.data = {}

    def create_resources(self, external):
        # Just return the external list
        return external or []

    def create_effects(self):
        pass

    def load(self):
        # Throw each resource into their respective pools
        for meta in self.create_resources():
            resources.add(meta)

        for meta, resource in resources.textures.load_pool():
            self.textures[meta.label] = resource

        for meta, resource in resources.shaders.load_pool():
            self.programs[meta.label] = resource

        for meta, resource in resources.scenes.load_pool():
            self.scenes[meta.label] = resource

        for meta, resource in resources.data.load_pool():
            self.data[meta.label] = resource

        self.create_effects()

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
