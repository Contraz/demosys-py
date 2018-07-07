
def setup(settings_override=None):
    """
    Initialize effects and prepare for running

    :param settings_override: (dict) keyword overrides for settings
    """
    from demosys.effects.registry import effects
    from demosys.conf import settings
    if settings_override:
        settings.update(**settings_override)

    effects.polulate(settings.EFFECTS)


def run(*args, **kwargs):
    """Run"""
    from demosys import view
    view.run(*args, **kwargs)
