import os
from demosys.conf import settings
from demosys.timers.base import BaseTimer

try:
    from pygame import mixer
except ImportError:
    if not os.environ.get('DOCS_BUILDING'):
        raise ImportError("pygame is needed for music timer {}".format(os.environ.get('DOCS_BUILDING')))


class Timer(BaseTimer):
    """
    Timer based on the current position in a wav, ogg or mp3 using pygame.mixer.
    Path to the music file is configured in ``settings.MUSIC``.
    """
    def __init__(self, **kwargs):
        mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
        mixer.music.load(settings.MUSIC)
        self.paused = True
        self.pause_time = 0
        self.initialized = False
        super().__init__(**kwargs)

    def start(self):
        """Play the music"""
        if self.initialized:
            mixer.music.unpause()
        else:
            mixer.music.play()
            # FIXME: Calling play twice to ensure the music is actually playing
            mixer.music.play()
            self.initialized = True
        self.paused = False

    def pause(self):
        """Pause the music"""
        mixer.music.pause()
        self.pause_time = self.get_time()
        self.paused = True

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
            The current location in the music
        """
        mixer.music.stop()
        return self.get_time()

    def get_time(self) -> float:
        """
        Get the current position in the music in seconds
        """
        if self.paused:
            return self.pause_time

        return mixer.music.get_pos() / 1000.0

    def set_time(self, value: float):
        """
        Set the current time in the music in seconds causing the player
        to seek to this location in the file.
        """
        if value < 0:
            value = 0

        # mixer.music.play(start=value)
        mixer.music.set_pos(value)
