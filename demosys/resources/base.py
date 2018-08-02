"""
Base registry class
"""


class BaseRegistry:
    """
    Base registry class providing callback functionality
    for each registry type.
    """

    def __init__(self):
        self.file_map = {}
        self.file_meta = {}

    @property
    def count(self):
        return len(self.file_map)

    def load(self, path, **kwargs):
        """Loads a resource or return existing one"""
        raise NotImplementedError()

    def load_deferred(self, path, **kwargs):
        """Register a resource for deferred loading"""
        raise NotImplementedError()

    def load_pool(self):
        """
        Loads all the data files using the configured finders.
        """
        for path, data_file in self.file_map.items():
            if self.file_map[path] is None:
                self._load(self.file_meta[path])

    def delete(self, obj, destroy=False):
        """
        Remove an object from the pool.
        This only removes the reference and will not actually destroy the object itself
        """
        for path, data in self.file_map.items():
            if data == obj:
                del self.file_map[path]
                del self.file_meta[path]
                if destroy:
                    self._destroy(obj)
                break

    def _destroy(self, obj):
        """Destroys the object"""
        raise NotImplementedError()

    def flush(self, destroy=False):
        """Delete all resources"""
        for obj in list(self.file_map.values()):
            self.delete(obj, destroy=destroy)

    def _find_last_of(self, file_path, finders):
        """Find the last occurance of the file in finders"""
        found_path = None
        for finder in finders:
            path = finder.find(file_path)
            if path:
                found_path = path

        return found_path
