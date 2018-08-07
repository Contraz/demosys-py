from demosys.finders import base
from demosys.conf import settings


class FileSystemFinder(base.BaseFileSystemFinder):
    """Find shaders in ``SHADER_DIRS``"""
    settings_attr = 'SHADER_DIRS'


class EffectDirectoriesFinder(base.BaseEffectDirectoriesFinder):
    """Finds shaders in the registered effects"""
    directory = 'shaders'


def get_finders():
    for finder in settings.SHADER_FINDERS:
        yield base.get_finder(finder)
