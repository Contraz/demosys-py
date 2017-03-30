"""
Settings and configuration for demosys
"""
import importlib
import os

from demosys.conf import default_settings
from demosys.core.exceptions import ImproperlyConfigured

ENVIRONMENT_VARIABLE = "DEMOSYS_SETTINGS_MODULE"


class Settings:
    def __init__(self):
        settings_module = os.environ.get(ENVIRONMENT_VARIABLE)
        if not settings_module:
            raise ImproperlyConfigured(
                "Settings module environment variable not found. "
                "You must defined the environment variable {}".format(ENVIRONMENT_VARIABLE)
            )

        # Update this dict from global settings
        for setting in dir(default_settings):
            if setting.isupper():
                setattr(self, setting, getattr(default_settings, setting))

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

    def is_configured(self):
        return hasattr(self, 'SETTINGS_MODULE')

    def __repr__(self):
        return '<{cls} "{settings_module}>"'.format(
            cls=self.__class__.__name__,
            settings_module=self.SETTINGS_MODULE,
        )


settings = Settings()
