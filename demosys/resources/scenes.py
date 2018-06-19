"""Scene Regisry"""
from demosys.core.exceptions import ImproperlyConfigured
from demosys.core.scenefiles.finders import get_finders
from demosys.scene import Scene
from demosys.conf import settings
from demosys.utils.module_loading import import_string


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
        # Figure out what scene loader class should be used
        for loader_name in settings.SCENE_LOADERS:
            loader_cls = import_string(loader_name)
            if loader_cls.supports_file(path):
                if path not in self.scenes:
                    loader_cls = import_string(loader_name)
                    self.scenes[path] = Scene(path, loader=loader_cls(path), **kwargs)
                break
        else:
            raise ImproperlyConfigured("Scene {} has no loader class registered. Check settings.SCENE_LOADERS")

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
                raise ImproperlyConfigured("Cannot find scene {}".format(name))


scenes = Scenes()
