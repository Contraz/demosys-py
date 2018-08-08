from demosys.project.base import BaseProject
from demosys.effects.registry import effects


class Project(BaseProject):
    """
    The project what will be assigned when no project are specified.
    This is mainly used when the ``runeffect`` command is used
    """
    def __init__(self, effect_module):

        super().__init__()
        self.effect_module = effect_module
        self.effect = None

    def create_resources(self):
        pass

    def create_effect_instances(self):
        cls = self.get_runnable_effect()
        self.effect = self.create_effect('default', cls.__name__)

    def get_runnable_effect(self):
        """
        Attempt to get a runnable effect in a package
        """
        runnable = effects.packages[0].runnable_effects()
        return runnable[0]
