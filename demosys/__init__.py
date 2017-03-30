from demosys import view


def setup():
    from demosys.effects.registry import effects
    from demosys.conf import settings

    effects.polulate(settings.EFFECTS)


def run():
    view.run()
