

class SceneLoader:
    """Base class for object loaders"""
    def __init__(self, **kwargs):
        pass

    def load(self):
        """Loads and returns the scene"""
        raise NotImplemented
