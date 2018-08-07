from demosys.finders import base
from demosys.conf import settings


class FileSystemFinder(base.BaseFileSystemFinder):
    """Find shaders in ``PROGRAM_DIRS``"""
    settings_attr = 'PROGRAM_DIRS'


class EffectDirectoriesFinder(base.BaseEffectDirectoriesFinder):
    """Finds programs in registered effects"""
    directory = 'programs'


def get_finders():
    for finder in settings.PROGRAM_FINDERS:
        yield base.get_finder(finder)
