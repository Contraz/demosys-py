from pathlib import Path
from typing import Union

from demosys import context
from demosys.scene import Scene


class SceneLoader:
    """Base class for object loaders"""
    # File extensions supported by this loader
    file_extensions = []

    def __init__(self, path: Union[str, Path], **kwargs):
        self.path = path
        self.ctx = context.ctx()

    def load(self, scene: Scene, path: Path=None):
        """
        Deferred loading of the scene

        :param scene: The scene object
        :param file: Resolved path if changed by finder
        """
        raise NotImplementedError()

    @classmethod
    def supports_file(cls, path: Path):
        """Check if the loader has a supported file extension"""
        for ext in cls.file_extensions:
            if path.suffixes[:len(ext)] == ext:
                return True

        return False
