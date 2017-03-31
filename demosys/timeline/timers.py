import glfw
from pygame import mixer


class Timer:
    """Timer based on glfw time"""
    def __init__(self, **kwargs):
        self.start_time = None
        self.stop_time = None
        self.pause_time = None
        self.offset = 0

    def start(self):
        # Initial start?
        if self.start_time is None:
            self.start_time = glfw.get_time()
        # Play after pause
        else:
            # Add the duration of the paused interval to the total offset
            pause_duration = glfw.get_time() - self.pause_time
            self.offset += pause_duration
            # print("pause duration", pause_duration, "offset", self.offset)
            # Exit the paused state
            self.pause_time = None

    def pause(self):
        self.pause_time = glfw.get_time()

    def toggle_pause(self):
        if self.pause_time:
            self.start()
        else:
            self.pause()

    def stop(self):
        self.stop_time = glfw.get_time()
        return self.stop_time - self.start_time - self.offset

    def get_time(self):
        if self.pause_time is not None:
            time = self.pause_time - self.offset - self.start_time
            return time

        time = glfw.get_time()
        return time - self.start_time - self.offset


class MusicTimer:
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
