from rocket import Rocket
from rocket.controllers import TimeController

from demosys.conf import settings
from demosys.resources import tracks
from demosys.timers.base import BaseTimer


class Timer(BaseTimer):
    """
    Basic rocket timer.
    Sets up rocket using values in ``settings.ROCKET``.
    The current time is translated internally in rocket
    to row positions based on the configured rows per second (RPS).
    """
    def __init__(self, **kwargs):
        """Initialize the rocket timer using values from settings"""
        config = getattr(settings, 'ROCKET', None)
        if config is None:
            config = {}

        self.mode = config.get('mode') or 'editor'
        self.files = config.get('files') or './tracks'
        self.project = config.get('project') or 'project.xml'
        self.rps = config.get('rps', 24)
        self.start_paused = False

        self.controller = TimeController(self.rps)
        if self.mode == 'editor':
            self.rocket = Rocket.from_socket(self.controller, track_path=self.files)
            self.start_paused = True
        elif self.mode == 'project':
            self.rocket = Rocket.from_project_file(self.controller, self.project)
        elif self.mode == 'files':
            self.rocket = Rocket.from_files(self.controller, self.files)
        else:
            raise ValueError("Unknown rocket mode: '{}'".format(self.mode))

        # Register tracks in the editor
        # Ninja in pre-created track objects
        for track in tracks.tacks:
            self.rocket.tracks.add(track)

        # Tell the editor about these tracks
        for track in tracks.tacks:
            self.rocket.track(track.name)

        self.rocket.update()
        super().__init__(**kwargs)

    def start(self):
        """Start the timer"""
        if not self.start_paused:
            self.rocket.start()

    def get_time(self) -> float:
        """
        Get the current time in seconds

        Returns:
            The current time in seconds
        """
        self.rocket.update()
        return self.rocket.time

    def set_time(self, value: float):
        """
        Set the current time jumping in the timeline.

        Args:
            value (float): The new time
        """
        if value < 0:
            value = 0

        self.controller.row = self.rps * value

    def pause(self):
        """Pause the timer"""
        self.controller.playing = False

    def toggle_pause(self):
        """Toggle pause mode"""
        self.controller.playing = not self.controller.playing

    def stop(self) -> float:
        """
        Stop the timer

        Returns:
            The current time.
        """
        return self.rocket.time
