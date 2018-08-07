"""
Registry general data files
"""
from demosys.conf import settings
from demosys.resources.base import BaseRegistry, ResourceDescription
from demosys.utils.module_loading import import_string


class DataDescription(ResourceDescription):
    require_label = True
    default_loader = 'binary'

    def __init__(self, path=None, label=None, loader=None, **kwargs):
        kwargs.update({
            "path": path,
            "label": label,
            "loader": loader,
        })
        super().__init__(kwargs)


class DataFiles(BaseRegistry):
    """Registry for requested data files"""
    def __init__(self):
        super().__init__()
        self._loaders = [
            import_string(loader) for loader in settings.DATA_LOADERS
        ]


data = DataFiles()
