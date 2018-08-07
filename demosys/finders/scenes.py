from demosys.finders import base
from demosys.conf import settings


class FileSystemFinder(base.BaseFileSystemFinder):
    """Find textures in ``SCENE_DIRS``"""
    settings_attr = 'SCENE_DIRS'


class EffectDirectoriesFinder(base.BaseEffectDirectoriesFinder):
    """Finds textures in the registered effects"""
    directory = 'scenes'


def get_finders():
    for finder in settings.SCENE_FINDERS:
        yield base.get_finder(finder)
