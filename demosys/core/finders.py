"""
Base finders
"""
import os
from collections import namedtuple
from demosys.conf import settings
from demosys.core.exceptions import ImproperlyConfigured

FinderEntry = namedtuple('FinderEntry', ['path', 'abspath', 'exists'])


class BaseFileSystemFinder:
    """Base class for searching directory lists"""
    settings_attr = None

    def __init__(self):
        if not hasattr(settings, self.settings_attr):
            raise ImproperlyConfigured(
                "Settings module don't define TEXTURE_DIRS."
                "This is required when using a FileSystemFinder."
            )
        self.paths = getattr(settings, self.settings_attr)

        self._cache = {}

    def find(self, path):
        """
        Find a file in the path.
        When creating a custom finder, this is the method you override.

        :param path: The path to find
        :return: The absolute path to the file or None if not found
        """
        return self._find(path)

    def _find(self, path):
        """
        Similar to ``find()``, but it caches each result to speed things.

        :param path: The path to find
        :return: The absolute path to the file or None if not found
        """
        for entry in self.paths:
            abspath = os.path.join(entry, path)
            if os.path.exists(abspath):
                self.cache(abspath, abspath)
                return abspath
            else:
                self.cache(abspath, abspath, exists=False)

        return None

    def find_cached(self, path):
        """
        Check if the path is already cached.
        This method should normally not be overridden.

        :param path: The path to the file
        :return: The absolute path to the file or None
        """
        entry = self._cache.get(path)

        if entry.exists:
            return entry.abspath

        return None

    def cache(self, path, abspath, exists=True):
        """
        Caches an entry.
        Should ideally not be overridden.

        :param path: The path
        :param abspath: The absolute path
        :param exists: Did the file exist? (bool)
        """
        self._cache[path] = FinderEntry(path=path, abspath=abspath, exists=exists)


class BaseEffectDirectoriesFinder(BaseFileSystemFinder):
    """Base class for searching effect directories"""
    directory = None

    def __init__(self):
        from demosys.effects.registry import effects
        self.paths = list(effects.get_dirs())
        self._cache = {}

    def find(self, path):
        return self._find(os.path.join(self.directory, path))
