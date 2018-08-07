from demosys.finders import base
from demosys.conf import settings


class FileSystemFinder(base.BaseFileSystemFinder):
    """Find data in ``DATA_DIRS``"""
    settings_attr = 'DATA_DIRS'


class EffectDirectoriesFinder(base.BaseEffectDirectoriesFinder):
    """Finds data in the registered effects"""
    directory = 'data'


def get_finders():
    for finder in settings.DATA_FINDERS:
        yield base.get_finder(finder)
