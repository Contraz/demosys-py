from demosys.core import finders
from demosys.conf import settings


class FileSystemFinder(finders.BaseFileSystemFinder):
    """Find data in ``DATA_DIRS``"""
    settings_attr = 'DATA_DIRS'


class EffectDirectoriesFinder(finders.BaseEffectDirectoriesFinder):
    """Finds data in the registered effects"""
    directory = 'data'


def get_finders():
    for finder in settings.DATA_FINDERS:
        yield finders.get_finder(finder)
