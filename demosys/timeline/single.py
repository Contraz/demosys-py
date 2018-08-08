from demosys.timeline.base import BaseTimeline


class Timeline(BaseTimeline):
    """Run a single effect"""
    def __init__(self, project, **kwargs):
        super().__init__(project)

    def get_active_effect(self, time):
        return self._project.effect

    def draw(self, time, frametime, target):
        effect = self.get_active_effect(time)
        effect.draw(time, frametime, target)

    def key_event(self, key, scancode, action, mods):
        print("Timeline:key_event", key, scancode, action, mods)
