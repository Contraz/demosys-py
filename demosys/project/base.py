from demosys import context
from demosys import resources
from demosys.effects.registry import effects


class BaseProject:
    """The Project"""
    effect_packages = []
    resources = []
    override_resources = {}

    def __init__(self):
        self._effects = {}
        self._programs = {}
        self._textures = {}
        self._scenes = {}
        self._data = {}

    def get_default_effect(self):
        raise NotImplementedError()

    def create_effect_classes(self):
        """Create effect classes in the registry"""
        effects.polulate(self.effect_packages)

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
        return self.resources

    def create_effect_instances(self):
        """
        Create instances of effects
        """
        raise NotImplementedError()

    def create_effect(self, label, name, *args, **kwargs):
        """Create an effect instance"""
        params = name.split('.')
        effect_cls = effects.find_effect_class(params[-1], package_name=".".join(params[:-1]))
        effect = effect_cls(*args, **kwargs)
        effect._label = label

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

    def reload_programs(self):
        print("Reloading programs:")
        for name, program in self._programs.items():
            if getattr(program, 'program', None):
                print(" - {}".format(program.meta.label))
                program.program = resources.programs.load(program.meta)

    def get_effect(self, label):
        return self._get_resource(label, self._effects, "effect")

    def get_effect_class(self, class_name, package_name=None):
        return effects.find_effect_class(class_name, package_name=package_name)

    def get_scene(self, label):
        return self._get_resource(label, self._scenes, "scene")

    def get_program(self, label):
        return self._get_resource(label, self._programs, "program")

    def get_texture(self, label):
        return self._get_resource(label, self._textures, "texture")

    def get_data(self, label):
        return self._get_resource(label, self._data, "data")

    def _get_resource(self, label, source, resource_type):
        try:
            return source[label]
        except KeyError:
            raise ValueError("Cannot find {0} with label '{1}'.\nExisting {0} labels: {2}".format(
                resource_type, label, list(source.keys())))

    def get_runnable_effects(self):
        """
        Returns all runnable effects in the project

        :return: List of all runnable effects
        """
        return [effect for name, effect in self._effects.items() if effect.runnable]

    @property
    def ctx(self):
        return context.ctx()
