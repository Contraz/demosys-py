from demosys.core import finders
from demosys.conf import settings


class FileSystemFinder(finders.BaseFileSystemFinder):
    """Find textures in ``TEXTURE_DIRS``"""
    settings_attr = 'TEXTURE_DIRS'


class EffectDirectoriesFinder(finders.BaseEffectDirectoriesFinder):
    """Finds textures in the registered effects"""
    directory = 'textures'


def get_finders():
    for finder in settings.TEXTURE_FINDERS:
        yield finders.get_finder(finder)
