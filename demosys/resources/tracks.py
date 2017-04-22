"""
Registry for rocket tracks
"""
from rocket.tracks import Track


class Tracks:
    """Registry for requested rocket tracks"""
    def __init__(self):
        self.tacks = []
        self.track_map = {}

    def get(self, name):
        """
        Get or create a Track object.

        :param name: Name of the track
        :return: Track object
        """
        name = name.lower()
        track = self.track_map.get(name)
        if not track:
            track = Track(name)
            self.tacks.append(track)
            self.track_map[name] = track
        return track

    def load(self):
        """
        Dummy. This will be handled by the rocket library,
        """
        pass


tracks = Tracks()
