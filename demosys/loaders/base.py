from typing import Any

from demosys import context
from demosys.finders import (data, program, textures, scenes)


class BaseLoader:
    """
    Base loader class for all resources
    """

    def __init__(self, meta):
        """
        :param meta: ResourceDescription instance
        """
        self.meta = meta

    def load(self) -> Any:
        """
        Load a resource

        :returns: The newly loaded resource
        """
        raise NotImplementedError()

    def find_data(self, path):
        return self._find_last_of(path, data.get_finders())

    def find_program(self, path):
        return self._find_last_of(path, program.get_finders())

    def find_texture(self, path):
        return self._find_last_of(path, textures.get_finders())

    def find_scene(self, path):
        return self._find_last_of(path, scenes.get_finders())

    def _find_last_of(self, path, finders):
        """Find the last occurance of the file in finders"""
        found_path = None
        for finder in finders:
            path = finder.find(path)
            if path:
                found_path = path

        return found_path

    @property
    def ctx(self):
        """ModernGL context"""
        return context.ctx()
