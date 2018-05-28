from .base import SceneLoader


class ObjLoader(SceneLoader):
    """Loade obj files"""
    file_extensions = ['.obj']

    def __init__(self, file_path):
        self.path = path
        super().__init__(file_path)

    def load(self, scene, file=None):
        print(scene, file)
        return scene
