import glfw
from pygame import mixer
from .base import Timer


class MusicTimer(Timer):
    """Timer based on music"""
    def __init__(self, **kwargs):
        mixer.init()
        mixer.music.load(kwargs['source'])
        self.paused = True
        # Reported time is not accurate when pausing or unpausing. We hack around it.
        self.pause_time = 0
        self.initialized = False
        self._upt = 0  # hack fixing jaggy unpause

    def start(self):
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
        if self.paused:
            self.start()
            self._upt = glfw.get_time()
        else:
            self.pause()

    def stop(self):
        mixer.music.stop()
        return self.get_time()

    def get_time(self):
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
