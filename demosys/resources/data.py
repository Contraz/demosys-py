"""
Registry general data files
"""
from demosys.core.exceptions import ImproperlyConfigured
from demosys.core.datafiles.finders import get_finders
from .base import BaseRegistry


class Data:
    """
    Generic data file.
    This can be extended with cusomtized loading functions.
    """
    def __init__(self, path, mode='binary'):
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


class DataFiles(BaseRegistry):
    """Registry for requested data files"""
    def __init__(self):
        super().__init__()
        self.files = []
        self.file_map = {}

    def get(self, name, create=False, cls=Data) -> Data:
        """
        Get or create a Data object.

        :param name: data file with relative path
        :param crate: (bool) register a new resource (or fetch existing)
        :param cls: (Data class) custom data class
        :return: Data object
        """
        if not hasattr(cls, 'load'):
            raise ImproperlyConfigured("{} must have a load(path) method".format(cls.__class__))

        key = name.lower()

        data_file = self.file_map.get(key)
        if not data_file:
            data_file = cls(name)
            self.files.append(data_file)
            self.file_map[key] = data_file

        return data_file

    def load(self):
        """
        Loads all the data files using the configured finders.
        """
        finders = list(get_finders())
        print("Loading data files:")
        for name, data_file in self.file_map.items():
            for finder in finders:
                path = finder.find(name)
                if path:
                    print(" - {}".format(path))
                    data_file.load(path)
                    break
            else:
                raise ImproperlyConfigured("Cannot find data file {}".format(name))

        self._on_loaded()


data = DataFiles()
