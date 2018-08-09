"""
Settings and configuration for demosys
"""
import importlib
import os
from demosys.conf import default
from demosys.exceptions import ImproperlyConfigured

ENVIRONMENT_VARIABLE = "DEMOSYS_SETTINGS_MODULE"

# pylint: disable=C0103


class Settings:
    SETTINGS_MODULE = None

    PROGRAM_DIRS = []
    TEXTURE_DIRS = []
    DATA_DIRS = []
    SCENE_DIRS = []

    def setup(self):
        settings_module = os.environ.get(ENVIRONMENT_VARIABLE)
        if not settings_module:
            raise ImproperlyConfigured(
                "Settings module environment variable not found. "
                "You must defined the environment variable {}".format(ENVIRONMENT_VARIABLE)
            )

        # Update this dict from global settings
        for setting in dir(default):
            if setting.isupper():
                setattr(self, setting, getattr(default, setting))

        # Read the supplied settings module
        self.SETTINGS_MODULE = settings_module
        module = importlib.import_module(self.SETTINGS_MODULE)
        if not module:
            raise ImproperlyConfigured(
                "Settings module '{}' not found. ".format(self.SETTINGS_MODULE)
            )

        for setting in dir(module):
            if setting.isupper():
                value = getattr(module, setting)
                # TODO: Add more validation here
                setattr(self, setting, value)

    def update(self, **kwargs):
        """Override settings values"""
        for name, value in kwargs.items():
            setattr(self, name, value)

    def is_configured(self):
        return hasattr(self, 'SETTINGS_MODULE')

    def __repr__(self):
        return '<{cls} "{settings_module}>"'.format(
            cls=self.__class__.__name__,
            settings_module=self.SETTINGS_MODULE,
        )

    def add_program_dir(self, directory):
        """Hack in program directory"""
        dirs = list(self.PROGRAM_DIRS)
        dirs.append(directory)
        self.PROGRAM_DIRS = dirs

    def add_texture_dir(self, directory):
        """Hack in texture directory"""
        dirs = list(self.TEXTURE_DIRS)
        dirs.append(directory)
        self.TEXTURE_DIRS = dirs

    def add_data_dir(self, directory):
        """Hack in a data directory"""
        dirs = list(self.DATA_DIRS)
        dirs.append(directory)
        self.DATA_DIRS = dirs


settings = Settings()
