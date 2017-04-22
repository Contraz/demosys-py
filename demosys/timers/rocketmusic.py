from .rocket import RocketTimer
from .music import MusicTimer


class RocketMusicTimer(RocketTimer):
    """Rocket timer playing music"""
    def __init__(self, **kwargs):
        self.music = MusicTimer()
        super().__init__(**kwargs)
