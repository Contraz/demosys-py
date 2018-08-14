from demosys.timers.music import Timer as MusicTimer
from demosys.timers.rocket import Timer as RocketTimer


class Timer(RocketTimer):
    """Rocket timer playing music"""
    def __init__(self, **kwargs):
        self.music = MusicTimer()
        super().__init__(**kwargs)

    def start(self):
        """Start the timer"""
        self.music.start()
        if not self.start_paused:
            self.rocket.start()

    def get_time(self):
        """Get the current time in seconds"""
        self.rocket.update()
        return self.music.get_time()

    def set_time(self, value):
        self.music.set_time(value)

    def pause(self):
        """Pause the timer"""
        self.controller.playing = False
        self.music.pause()

    def toggle_pause(self):
        """Toggle pause mode"""
        self.controller.playing = not self.controller.playing
        self.music.toggle_pause()

    def stop(self):
        """Stop the timer"""
        return self.rocket.time
