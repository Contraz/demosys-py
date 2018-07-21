import moderngl

# Window instance shortcut
WINDOW = None  # noqa


def window() -> 'demosys.context.base.Window':
    """The window instance we are rendering to"""
    if not WINDOW:
        raise RuntimeError("Attempting to get window before creation")

    return WINDOW


def ctx() -> moderngl.Context:
    """ModernGL context"""
    win = window()
    if not win.ctx:
        raise RuntimeError("Attempting to get context before creation")

    return win.ctx
