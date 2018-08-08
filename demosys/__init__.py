from demosys.conf import settings


def setup(**kwargs):
    """Initialize"""
    settings.update(**kwargs)


def run(*args, **kwargs):
    """Run"""
    from demosys import view
    view.run(*args, **kwargs)
