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
        return self._find(path)

    def _find(self, path):
        for p in self.paths:
            abspath = os.path.join(p, path)
            if os.path.exists(abspath):
                self.cache(abspath, abspath)
                return abspath
            else:
                self.cache(abspath, abspath, exists=False)

        return None

    def find_cached(self, path):
        e = self._cache.get(path)
        if e.exists:
            return e.abspath
        return None

    def cache(self, path, abspath, exists=True):
        self._cache[path] = FinderEntry(path=path, abspath=abspath, exists=exists)
