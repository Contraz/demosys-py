
def setup():
    from demosys.effects.registry import effects
    from demosys.conf import settings

    effects.polulate(settings.EFFECTS)


def run(*args, **kwargs):
    from demosys import view
    view.run(*args, **kwargs)
