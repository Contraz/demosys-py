import glfw
from .base import BaseTimer


class Timer(BaseTimer):
    """
    Timer based on glfw time.
    This is the default / most basic timer.
    """
    def __init__(self, **kwargs):
        self.start_time = None
        self.stop_time = None
        self.pause_time = None
        self.offset = 0
        super().__init__(**kwargs)

    def start(self):
        """Start the timer"""
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
        """Pause the timer"""
        self.pause_time = glfw.get_time()

    def toggle_pause(self):
        """Toggle pause"""
        if self.pause_time:
            self.start()
        else:
            self.pause()

    def stop(self):
        """Stop the timer"""
        self.stop_time = glfw.get_time()
        return self.stop_time - self.start_time - self.offset

    def get_time(self):
        """Get the current time in seconds"""
        if self.pause_time is not None:
            time = self.pause_time - self.offset - self.start_time
            return time

        time = glfw.get_time()
        return time - self.start_time - self.offset
