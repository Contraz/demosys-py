import time

from demosys.timers.base import BaseTimer


class Timer(BaseTimer):
    """
    Timer based on python ``time``.
    This is the default timer.
    """
    def __init__(self, **kwargs):
        self.start_time = None
        self.stop_time = None
        self.pause_time = None
        self.offset = 0
        super().__init__(**kwargs)

    def start(self):
        """
        Start the timer by recoding the current ``time.time()``
        preparing to report the number of seconds since this timestamp.
        """
        if self.start_time is None:
            self.start_time = time.time()
        # Play after pause
        else:
            # Add the duration of the paused interval to the total offset
            pause_duration = time.time() - self.pause_time
            self.offset += pause_duration
            # print("pause duration", pause_duration, "offset", self.offset)
            # Exit the paused state
            self.pause_time = None

    def pause(self):
        """
        Pause the timer by setting the internal pause time using ``time.time()``
        """
        self.pause_time = time.time()

    def toggle_pause(self):
        """Toggle the paused state"""
        if self.pause_time:
            self.start()
        else:
            self.pause()

    def stop(self) -> float:
        """
        Stop the timer

        Returns:
            The time the timer was stopped
        """
        self.stop_time = time.time()
        return self.stop_time - self.start_time - self.offset

    def get_time(self) -> float:
        """
        Get the current time in seconds

        Returns:
            The current time in seconds
        """
        if self.pause_time is not None:
            curr_time = self.pause_time - self.offset - self.start_time
            return curr_time

        curr_time = time.time()
        return curr_time - self.start_time - self.offset

    def set_time(self, value: float):
        """
        Set the current time. This can be used to jump in the timeline.

        Args:
            value (float): The new time
        """
        if value < 0:
            value = 0

        self.offset += self.get_time() - value
