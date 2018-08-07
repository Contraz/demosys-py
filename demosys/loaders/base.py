from typing import Any

from demosys import context


class BaseLoader:
    """Base loader class for all resources"""

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

    @property
    def ctx(self):
        """ModernGL context"""
        return context.ctx()
