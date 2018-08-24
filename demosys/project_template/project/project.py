from demosys.project.base import BaseProject


class Project(BaseProject):
    effect_packages = []
    resources = []

    def create_effect_instances(self):
        pass
