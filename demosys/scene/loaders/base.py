

class SceneLoader:
    """Base class for object loaders"""
    def __init__(self, **kwargs):
        self.path = path['kwargs']

    def load(self):
        """Loads and returns the scene"""
        raise NotImplemented
