from demosys.core import finders
from demosys.conf import settings


class FileSystemFinder(finders.BaseFileSystemFinder):
    """Find textures in ``SCENE_DIRS``"""
    settings_attr = 'SCENE_DIRS'


class EffectDirectoriesFinder(finders.BaseEffectDirectoriesFinder):
    """Finds textures in the registered effects"""
    directory = 'scenes'


def get_finders():
    for finder in settings.SCENE_FINDERS:
        yield finders.get_finder(finder)
