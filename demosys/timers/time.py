import glfw
from .base import BaseTimer


class Timer(BaseTimer):
    """Timer based on glfw time"""
    def __init__(self, **kwargs):
        self.start_time = None
        self.stop_time = None
        self.pause_time = None
        self.offset = 0
        super().__init__(**kwargs)

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
