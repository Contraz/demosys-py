"""
Registry general data files
"""
from demosys.conf import settings
from demosys.resources.base import BaseRegistry
from demosys.utils.module_loading import import_string


class DataFiles(BaseRegistry):
    """Registry for requested data files"""
    def __init__(self):
        super().__init__()
        self._loaders = [
            import_string(loader) for loader in settings.DATA_LOADERS
        ]


data = DataFiles()
