"""
Base finders
"""
import os
from collections import namedtuple

FinderEntry = namedtuple('FinderEntry', ['path', 'abspath', 'exists'])


class FileSystemFinder:
    """Find files in the local file system"""
    def __init__(self, paths):
        self.paths = paths
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
        for p in self.paths:
            abspath = os.path.join(p, path)
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
        e = self._cache.get(path)
        if e.exists:
            return e.abspath
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
