from demosys.timeline.base import BaseTimeline


class Timeline(BaseTimeline):
    """Run a single effect"""
    def __init__(self, project, *args, **kwargs):
        super().__init__(project)

    def draw(self, time, frametime, target):
        effect = self._project.get_default_effect()
        effect.draw(time, frametime, target)

    def key_event(self, key, action, mods):
        pass
