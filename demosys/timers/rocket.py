from rocket.controller import TimeController
from rocket.rocket import Rocket
from demosys.resources import tracks


class RocketTimer:
    """Basic rocket timer"""
    def __init__(self):
        self.controller = TimeController(24)
        self.rocket = Rocket(self.controller, track_path="./data")
        self.rocket.start()

        # Register tracks in the editor
        # Ninja in pre-created track objects
        for track in tracks.tacks:
            self.rocket.tracks.add(track)

        # Tell the editor about these tracks
        for track in tracks.tacks:
            self.rocket.track(track.name)

    def start(self):
        pass

    def get_time(self):
        self.rocket.update()
        return self.rocket.time

    def pause(self):
        self.controller.playing = False

    def toggle_pause(self):
        self.controller.playing = not self.controller.playing

    def stop(self):
        return self.rocket.time
