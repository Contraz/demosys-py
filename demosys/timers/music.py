import glfw
from demosys.conf import settings
from .base import BaseTimer

try:
    from pygame import mixer
except ImportError as e:
    print("pygame is needed for audio playback")


class MusicTimer(BaseTimer):
    """Timer based on music"""
    def __init__(self, **kwargs):
        mixer.init()
        mixer.music.load(settings.MUSIC)
        self.paused = True
        # Reported time is not accurate when pausing or unpausing. We hack around it.
        self.pause_time = 0
        self.initialized = False
        self._upt = 0  # hack fixing jaggy unpause
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
        self.pause_time = self.get_time()
        print("paused", self.pause_time)
        self.paused = True
        mixer.music.pause()

    def toggle_pause(self):
        """Toggle pause mode"""
        if self.paused:
            self.start()
            self._upt = glfw.get_time()
        else:
            self.pause()

    def stop(self):
        """Stop the music and the timer"""
        mixer.music.stop()
        return self.get_time()

    def get_time(self):
        """Get the current time in seconds"""
        # Hack around inaccuracy in mixer
        if self.paused:
            return self.pause_time

        time = mixer.music.get_pos() / 1000.0

        # Jaggy unpause. get_pos returns future and past time.
        # We inspect the difference between the paused time and
        # the reported time for 0.25 seconds after the unpause
        if glfw.get_time() < (self._upt + 0.25):
            if time > self.pause_time + 0.25:
                return self.pause_time

        if time < self.pause_time:
            return self.pause_time

        # Avoid jaggy time skips when unpausing
        if time < self.pause_time:
            return self.pause_time
        return time
