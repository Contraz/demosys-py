# import glfw
from demosys.conf import settings
from .base import BaseTimer

try:
    from pygame import mixer
except ImportError:
    print("pygame is needed for timer: MusicTimer")


class MusicTimer(BaseTimer):
    """Timer based on music"""
    def __init__(self, **kwargs):
        mixer.init(frequency=44100, size=-16, channels=2, buffer=1024)
        mixer.music.load(settings.MUSIC)
        self.paused = True
        self.pause_time = 0
        self.initialized = False
        super().__init__(**kwargs)

    def start(self):
        """Start the timer and music"""
        if self.initialized:
            mixer.music.unpause()
        else:
            mixer.music.play()
            # FIXME: Calling play twice to ensure the music is actually playing
            mixer.music.play()
            self.initialized = True
        self.paused = False

    def pause(self):
        mixer.music.pause()
        self.pause_time = self.get_time()
        self.paused = True

    def toggle_pause(self):
        """Toggle pause mode"""
        if self.paused:
            self.start()
        else:
            self.pause()

    def stop(self):
        """Stop the music and the timer"""
        mixer.music.stop()
        return self.get_time()

    def get_time(self):
        """Get the current time in seconds"""

        if self.paused:
            return self.pause_time

        return mixer.music.get_pos() / 1000.0
