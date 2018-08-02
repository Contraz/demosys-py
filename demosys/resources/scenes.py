"""Scene Regisry"""
from pathlib import Path
from typing import Union

from demosys.conf import settings
from demosys.core.exceptions import ImproperlyConfigured
from demosys.core.scenefiles.finders import get_finders
from demosys.scene import Scene
from demosys.utils.module_loading import import_string

from .base import BaseRegistry


class SceneMeta:

    def __init__(self, path, loader_cls, **kwargs):
        self.path = path
        self.loader_cls = loader_cls
        self.kwargs = kwargs


class Scenes(BaseRegistry):
    """
    A registry for scense requested by effects.
    Once all effects are initialized, we ask this class to load the scenes.
    """
    def __init__(self):
        super().__init__()
        self.scene_loaders = [
            import_string(loader) for loader in settings.SCENE_LOADERS
        ]

    def get(self, path: Union[str, Path], **kwargs) -> Scene:
        """Compatibility function for the old resource system"""
        return self.load(path, **kwargs)

    def load(self, path: Union[str, Path], **kwargs) -> Scene:
        """
        Get or create a scene object.
        This may return an empty object that will be filled during load
        based on the ``create`` parameter.

        :param path: Path to the scene file(s)
        :param create: (bool) Create an empty scene object if it doesn't exist
        :return: Scene object
        """
        path = Path(path)

        scene = self.file_map.get(path)
        if scene:
            return scene

        meta = self.load_deferred(path, **kwargs)
        scene = self._load(meta)

        return scene

    def load_deferred(self, path: Union[str, Path], **kwargs) -> SceneMeta:
        # Figure out what scene loader class should be used
        for loader_cls in self.scene_loaders:
            if loader_cls.supports_file(path):
                break
        else:
            raise ImproperlyConfigured(
                "Scene {} has no loader class registered. Check settings.SCENE_LOADERS".format(path))

        meta = SceneMeta(path, loader_cls, **kwargs)

        self.file_meta[path] = meta
        self.file_map[path] = None

        return meta

    def _load(self, meta) -> Scene:
        found_path = self._find_last_of(meta.path, list(get_finders()))

        if not found_path:
            raise ImproperlyConfigured("Cannot find scene file {}".format(meta.path))

        print("Loading: {}".format(meta.path))
        scene = Scene(meta.path, **meta.kwargs)
        scene.load(meta.loader_cls(meta.path), found_path)

        self.file_map[meta.path] = scene
        return scene

    def _destroy(self, obj):
        obj.destroy()


scenes = Scenes()
