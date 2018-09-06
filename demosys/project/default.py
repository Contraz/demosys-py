from demosys.project.base import BaseProject
from demosys.effects.registry import effects, parse_package_string


class Project(BaseProject):
    """
    The project what will be assigned when no project are specified.
    This is mainly used when the ``runeffect`` command is used
    """
    def __init__(self, effect_package):
        super().__init__()
        self.path = effect_package
        self.effect_package_name, self.effect_class_name = parse_package_string(effect_package)
        self.effect_packages = [self.effect_package_name]
        self.effect = None

    def get_default_effect(self):
        return self.effect

    def create_resources(self):
        pass

    def create_effect_instances(self):
        if self.effect_class_name:
            cls = effects.find_effect_class(self.path)
            if not cls.runnable:
                raise ValueError("Effect doesn't have the runnable flag set:", self.path)
        else:
            effect_package = effects.get_package(self.effect_package_name)
            runnable_effects = effect_package.runnable_effects()

            if not runnable_effects:
                raise ValueError("No runnable effects found in effect package", self.effect_package_name)

            cls = runnable_effects[-1]

        self.effect = self.create_effect('default', cls.__name__)
