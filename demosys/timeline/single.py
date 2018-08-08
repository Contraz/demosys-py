from demosys.timeline.base import BaseTimeline


class Timeline(BaseTimeline):
    """Run a single effect"""
    def __init__(self, project, **kwargs):
        super().__init__(project)
        self.active_effect = project.get_first_runnable_effect()

    def get_active_effect(self, time):
        return self.active_effect

    def draw(self, time, frametime, target):
        effect = self.get_active_effect(time)
        effect.draw(time, frametime, target)

    def key_event(self, key, scancode, action, mods):
        print("Timeline:key_event", key, scancode, action, mods)
