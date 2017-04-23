from .base import SceneLoader


class ObjLoader(SceneLoader):
    """Loade obj files"""
    def __init__(self, path=None):
        self.path = path
        super().__init__(path=path)

    def load(self):
        """
        Load an obj file

        :return: VAO containing the object
        """
        pass
