from demosys.timeline.base import BaseTimeline


class Timeline(BaseTimeline):
    """Run a single effect"""
    def __init__(self):
        self.active_effect = None

    def draw(self, time, frametime, target):
        self.active_effect.draw(time, frametime, target)

    def key_event(self, key, scancode, action, mods):
        print("Timeline:key_event", key, scancode, action, mods)
