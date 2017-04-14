"""
Registry for rocket tracks
"""
from rocket.tracks import Track


class Tracks:
    def __init__(self):
        self.tacks = []
        self.track_map = {}

    def get(self, name):
        name = name.lower()
        track = self.track_map.get(name)
        if not track:
            track = Track(name)
            self.tacks.append(track)
            self.track_map[name] = track
        return track

    def load(self):
        pass


tracks = Tracks()
