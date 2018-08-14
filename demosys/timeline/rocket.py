from .base import BaseTimeline


class Timeline(BaseTimeline):
    """
    At attempt to use rocket data as our timeline.
    We use rocket track values of 0 and 1 deciding if the effect should be active.
    Only runnable effects will be used.
    Each effect should also have some way to specify its draw priority

    The following class attributes must be specified on the effect:

        rocket_timeline_track = Track instance
        rocket_timeline_order = 0

    Effects are drawn in the user-defined order.

    We might want to eventually convert this timeline data into a more managable format
    internally because rocket tracks are not ideal for this in larger projects.
    """
    def __init__(self, project, *args, **kwargs):
        super().__init__(project)

        # Get all runnable effect sorting them by rocket_timeline_order
        self.effects = self._project.get_runnable_effects()
        self.effects.sort(key=lambda x: x.rocket_timeline_order)

    def draw(self, time, frametime, target):
        """
        Fetch track value for every runnable effect.
        If the value is > 0.5 we draw it.
        """
        for effect in self.effects:
            value = effect.rocket_timeline_track.time_value(time)
            if value > 0.5:
                effect.draw(time, frametime, target)
