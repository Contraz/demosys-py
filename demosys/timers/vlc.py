import os
from demosys.conf import settings
from .base import BaseTimer

try:
    import vlc
except ImportError:
    if not os.environ.get('DOCS_BUILDING'):
        raise ImportError("python-vlc is needed for vlc timer")


class Timer(BaseTimer):
    """
    Timer based on the python-vlc wrapper.
    Plays the music file defined in ``settings.MUSIC``.
    Requires ``python-vlc`` to be installed including the vlc application.
    """
    def __init__(self, **kwargs):
        self.player = vlc.MediaPlayer(settings.MUSIC)
        self.paused = True
        self.pause_time = 0
        self.initialized = False
        super().__init__(**kwargs)

    def start(self):
        """Start the music"""
        self.player.play()
        self.paused = False

    def pause(self):
        """Pause the music"""
        self.pause_time = self.get_time()
        self.paused = True
        self.player.pause()

    def toggle_pause(self):
        """Toggle pause mode"""
        if self.paused:
            self.start()
        else:
            self.pause()

    def stop(self) -> float:
        """
        Stop the music

        Returns:
            The current time in seconds
        """
        self.player.stop()
        return self.get_time()

    def get_time(self) -> float:
        """
        Get the current time in seconds

        Returns:
            The current time in seconds
        """
        if self.paused:
            return self.pause_time

        return self.player.get_time() / 1000.0
