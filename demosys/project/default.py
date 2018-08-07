from demosys.project.base import BaseProject


class Project(BaseProject):
    """
    The project what will be assigned when no project are specified.
    This is mainly used when the ``runeffect`` command is used
    """
    def __init__(self, effect_module):

        super().__init__()
        self.effect_moduele = effect_module

    def create_resources(self, external):
        # Ensure external resources are loaded
        pass

    def create_effects(self):
        # Create the effect instance
        pass
