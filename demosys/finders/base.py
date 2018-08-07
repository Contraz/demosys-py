"""
Base finders
"""
import functools
from collections import namedtuple
from pathlib import Path

from demosys.conf import settings
from demosys.exceptions import ImproperlyConfigured
from demosys.utils.module_loading import import_string

FinderEntry = namedtuple('FinderEntry', ['path', 'abspath', 'exists'])


class BaseFileSystemFinder:
    """Base class for searching directory lists"""
    settings_attr = None

    def __init__(self):
        if not hasattr(settings, self.settings_attr):
            raise ImproperlyConfigured(
                "Settings module don't define {}."
                "This is required when using a FileSystemFinder.".format(self.settings_attr)
            )
        self.paths = getattr(settings, self.settings_attr)

    def find(self, path: Path):
        """
        Find a file in the path. The file may exist in multiple
        paths. The last found file will be returned.

        :param path: The path to find
        :return: The absolute path to the file or None if not found
        """
        # Update paths from settings to make them editable runtime
        # This is only possible for FileSystemFinders
        if getattr(self, 'settings_attr', None):
            self.paths = getattr(settings, self.settings_attr)

        path_found = None

        for entry in self.paths:
            abspath = entry / path
            if abspath.exists():
                path_found = abspath

        return path_found


class BaseEffectDirectoriesFinder(BaseFileSystemFinder):
    """Base class for searching effect directories"""
    directory = None

    def __init__(self):
        pass

    def find(self, path: Path):
        path = Path(self.directory) / Path(path)
        return super().find(path)

    @property
    def paths(self):
        from demosys.effects.registry import effects
        return list(effects.get_dirs())


@functools.lru_cache(maxsize=None)
def get_finder(import_path):
    """
    Get a finder class from an import path.
    Raises ``demosys.core.exceptions.ImproperlyConfigured`` if the finder is not found.
    This function uses an lru cache.

    :param import_path: string representing an import path
    :return: An instance of the finder
    """
    Finder = import_string(import_path)
    if not issubclass(Finder, BaseFileSystemFinder):
        raise ImproperlyConfigured('Finder {} is not a subclass of core.finders.FileSystemFinder'.format(import_path))
    return Finder()
