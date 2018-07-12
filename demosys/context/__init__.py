import moderngl

# Window instance shortcut
WINDOW = None  # noqa


def window() -> 'demosys.context.base.Window':
    """The window instance we are rendering to"""
    return WINDOW


def ctx() -> moderngl.Context:
    """ModernGL context"""
    return WINDOW.ctx
