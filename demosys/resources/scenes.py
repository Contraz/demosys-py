"""Scene Regisry"""
from demosys.scene.loaders import gltf
from demosys.core.exceptions import ImproperlyConfigured
from demosys.core.scenefiles.finders import get_finders
from demosys.scene import Scene


class Scenes:
    """
    A registry for scense requested by effects.
    Once all effects are initialized, we ask this class to load the scenes.
    """
    def __init__(self):
        self.scenes = {}

    @property
    def count(self):
        return len(self.scenes)

    def get(self, path, create=False, **kwargs):
        """
        Get or create a scene object.
        This may return an empty object that will be filled during load
        based on the ``create`` parameter.

        :param path: Path to the scene file(s)
        :param create: (bool) Create an empty scene object if it doesn't exist
        :return: Scene object
        """
        # FIXME: Figure out what scene loader class should be used instead of hardcoding gltf
        # FIXME: This should be configured in settings
        if path not in self.scenes:
            self.scenes[path] = Scene(path, loader=gltf.GLTF2(path), **kwargs)

        return self.scenes[path]

    def load(self):
        finders = list(get_finders())
        print("Loading scenes:")
        for name, scene in self.scenes.items():
            for finder in finders:
                path = finder.find(name)
                if path:
                    print(" - {}".format(path))
                    scene.load(path)
                    break
            else:
                raise ImproperlyConfigured("Cannot find texture {}".format(name))


scenes = Scenes()
