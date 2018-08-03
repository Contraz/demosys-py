from demosys.core import finders
from demosys.conf import settings


class FileSystemFinder(finders.BaseFileSystemFinder):
    """Find shaders in ``SHADER_DIRS``"""
    settings_attr = 'SHADER_DIRS'


class EffectDirectoriesFinder(finders.BaseEffectDirectoriesFinder):
    """Finds shaders in the registered effects"""
    directory = 'shaders'


def get_finders():
    for finder in settings.SHADER_FINDERS:
        yield finders.get_finder(finder)
