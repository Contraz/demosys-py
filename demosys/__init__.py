from demosys.conf import settings
from demosys import view

__version__ = "2.1.0"


def setup(**kwargs):
    """Configure"""
    settings.setup()
    settings.update(**kwargs)


def init(*args, **kwargs):
    """Initialize and load"""
    view.init(*args, **kwargs)


def run(*args, **kwargs):
    """Run"""
    view.run(*args, **kwargs)
