from demosys.finders import base
from demosys.conf import settings


class FileSystemFinder(base.BaseFileSystemFinder):
    """Find textures in ``TEXTURE_DIRS``"""
    settings_attr = 'TEXTURE_DIRS'


class EffectDirectoriesFinder(base.BaseEffectDirectoriesFinder):
    """Finds textures in the registered effects"""
    directory = 'textures'


def get_finders():
    for finder in settings.TEXTURE_FINDERS:
        yield base.get_finder(finder)
