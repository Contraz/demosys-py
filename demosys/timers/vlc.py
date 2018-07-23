from demosys.conf import settings
from .base import BaseTimer

try:
    import vlc
except ImportError:
    print("python-vlc is needed for timer: VLCTimer")


class VLCTimer(BaseTimer):
    """Timer based on music"""
    def __init__(self, **kwargs):
        self.player = vlc.MediaPlayer(settings.MUSIC)
        self.paused = True
        self.pause_time = 0
        self.initialized = False
        super().__init__(**kwargs)

    def start(self):
        """Start the timer and music"""
        self.player.play()
        self.paused = False

    def pause(self):
        self.pause_time = self.get_time()
        self.paused = True
        self.player.pause()

    def toggle_pause(self):
        """Toggle pause mode"""
        if self.paused:
            self.start()
        else:
            self.pause()

    def stop(self):
        """Stop the music and the timer"""
        self.player.stop()
        return self.get_time()

    def get_time(self):
        """Get the current time in seconds"""
        # Hack around inaccuracy in mixer
        if self.paused:
            return self.pause_time

        return self.player.get_time() / 1000.0
