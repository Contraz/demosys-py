import moderngl

from demosys.conf import settings
from demosys.utils.module_loading import import_string
from demosys.context.base import BaseWindow

# Window instance shortcut
WINDOW = None  # noqa


def window(raise_on_error=True) -> BaseWindow:
    """
    The window instance we are rendering to

    :param raise_on_error: Raise an error if the window is not created yet
    """
    if not WINDOW and raise_on_error:
        raise RuntimeError("Attempting to get window before creation")

    return WINDOW


def ctx() -> moderngl.Context:
    """ModernGL context"""
    win = window()
    if not win.ctx:
        raise RuntimeError("Attempting to get context before creation")

    return win.ctx


def create_window():
    if window(raise_on_error=False):
        raise RuntimeError("Attempting to create window twice")

    window_cls_name = settings.WINDOW.get('class', 'demosys.context.pyqt.Window')
    window_cls = import_string(window_cls_name)
    new_window = window_cls()
    new_window.print_context_info()
    return new_window
