
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
    window = create_window()
    kwargs['window'] = window

    from demosys import view
    view.run(*args, **kwargs)


def create_window():
    from demosys.conf import settings
    from demosys.utils import module_loading

    window_cls_name = settings.WINDOW.get('class', 'demosys.context.glfw.GLFW_Window')
    print("window class", window_cls_name)
    window_cls = module_loading.import_string(window_cls_name)
    window = window_cls()
    window.print_context_info()
    return window
