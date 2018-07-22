import functools

from demosys.core import finders
from demosys.conf import settings
from demosys.core.exceptions import ImproperlyConfigured
from demosys.utils.module_loading import import_string


class FileSystemFinder(finders.BaseFileSystemFinder):
    """Find textures in ``SCENE_DIRS``"""
    settings_attr = 'SCENE_DIRS'


class EffectDirectoriesFinder(finders.BaseEffectDirectoriesFinder):
    """Finds textures in the registered effects"""
    directory = 'scenes'


def get_finders():
    for finder in settings.SCENE_FINDERS:
        yield get_finder(finder)


@functools.lru_cache(maxsize=None)
def get_finder(import_path):
    """
    Get a finder class from an import path.
    Raises ``demosys.core.exceptions.ImproperlyConfigured`` if the finder is not found.
    This function uses an lru cache.

    :param import_path: string representing an import path
    :return: An instance of the finder
    """
    Finder = import_string(import_path)
    if not issubclass(Finder, finders.BaseFileSystemFinder):
        raise ImproperlyConfigured('Finder {} is not a subclass of core.finders.FileSystemFinder'.format(import_path))
    return Finder()
