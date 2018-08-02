"""
Registry general data files
"""
from pathlib import Path

from demosys.core.exceptions import ImproperlyConfigured
from demosys.core.datafiles.finders import get_finders
from .base import BaseRegistry


class Data:
    """
    Generic data file.
    This can be extended with cusomtized loading functions.
    """
    def __init__(self, path, mode='binary', **kwargs):
        """
        :param path: file with relative path
        :param mode: What mode the file should be read ('b': binary, 't': text)
        """
        self.path = path
        self.mode = mode
        self.data = None

        load_funcs = self._get_load_funcs()
        try:
            self.func = load_funcs[mode]
        except KeyError:
            raise ImproperlyConfigured(
                "{} doesn't support mode '{}'. Options are {}".format(self.__class__, mode, load_funcs.keys())
            )

    def load(self, path):
        self.func(path)

    def destroy(self):
        self.data = None

    def load_binary(self, path):
        with open(path, 'rb') as fd:
            self.data = fd.read()

    def load_text(self, path):
        with open(path, 'r') as fd:
            self.data = fd.read()

    def _get_load_funcs(self):
        """Build a list of functions with prefix ``load_``"""
        return {"_".join(attr.split("_")[1:]): getattr(self, attr)
                for attr in dir(self)
                if attr.startswith("load_")}


class DataFileMeta:

    def __init__(self, path, cls, mode, **kwargs):
        self.path = path
        self.cls = cls
        self.mode = mode
        self.kwargs = kwargs


class DataFiles(BaseRegistry):
    """Registry for requested data files"""
    def __init__(self):
        super().__init__()

    def get(self, path: str, cls=Data, mode='binary', **kwargs) -> Data:
        """Compatibility function for the old resource system"""
        return self.load(path, cls=cls, mode=mode, **kwargs)

    def load(self, path: str, cls=Data, mode='binary', **kwargs) -> Data:
        """
        Load Data object or get existing

        :param path: data file with path (pathlib.Path)
        :param crate: (bool) register a new resource (or fetch existing)
        :param cls: (Data class) custom data class
        :return: Data object
        """
        path = Path(path)

        data_file = self.file_map.get(path)
        if data_file:
            return data_file

        meta = self.load_deferred(path, cls=cls, mode=mode, **kwargs)
        data_file = self._load(meta)

        return data_file

    def load_deferred(self, path: str, cls=Data, mode='binary', **kwargs):
        """
        Register a resource to be loaded in the loading stage

        :returns: DateFileMeta object
        """
        if not hasattr(cls, 'load'):
            raise ImproperlyConfigured("{} must have a load(path) method".format(cls.__class__))

        meta = DataFileMeta(path, cls, mode, **kwargs)

        self.file_map[path] = None
        self.file_meta[path] = meta

        return meta

    def _load(self, meta) -> Data:
        """Internal loader"""
        found_path = self._find_last_of(meta.path, list(get_finders()))

        if not found_path:
            raise ImproperlyConfigured("Cannot find data file {}".format(meta.path))

        print("Loading: {}".format(meta.path))
        data_file = meta.cls(meta.path, mode=meta.mode, **meta.kwargs)
        data_file.load(found_path)
        self.file_map[meta.path] = data_file

        return data_file

    def _destroy(self, obj):
        obj.destroy()


data = DataFiles()
