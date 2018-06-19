

class SceneLoader:
    """Base class for object loaders"""
    # File extensions supported by this loader
    file_extensions = []

    def __init__(self, file_path, **kwargs):
        self.file_path = file_path

    def load(self, scene, file=None):
        """
        Deferred loading of the scene

        :param scene: The scene object
        :param file: Resolved path if changed by finder
        """
        raise NotImplemented

    @classmethod
    def supports_file(cls, path):
        """Check if the loader has a supported file extension"""
        for ext in cls.file_extensions:
            if path.endswith(ext):
                return True

        return False
