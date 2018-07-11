import moderngl
from .base import Window

# Window instance shortcut
WINDOW = None  # noqa


def window() -> Window:
    """The window instance we are rendering to"""
    return WINDOW


def ctx() -> moderngl.Context:
    """ModernGL context"""
    return WINDOW.ctx
