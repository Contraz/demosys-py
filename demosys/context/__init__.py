import moderngl

# Window instance shortcut
WINDOW = None  # noqa


def ctx() -> moderngl.Context:
    """Get the moderngl context for the window"""
    return WINDOW.ctx
