import platform
import os

import moderngl
import pyglet

from demosys import context
from demosys.context.base import BaseWindow

from .keys import Keys

if platform.system() == "Darwin" and not os.environ.get('DOCS_BUILDING'):
    raise RuntimeError((
        "Pyglet do not support OpenGL core contexts "
        "and will only be able to support version 2.1 on OS X.\n"
        "Please use another window driver for this platform"
    ))


class Window(BaseWindow):
    """
    Window based on pyglet.

    Note that pylget is unable to make core 3.3+ contexts
    and will not work for certain drivers and enviroments such as on OS X.
    """
    keys = Keys

    def __init__(self):
        """
        Opens a window using pyglet, registers input callbacks
        and creates a moderngl context.
        """
        super().__init__()
        # Disable all error checking
        pyglet.options['debug_gl'] = False

        # Set context parameters
        config = pyglet.gl.Config()
        config.double_buffer = True
        config.major_version = self.gl_version.major
        config.minor_version = self.gl_version.minor
        config.forward_compatible = True
        config.sample_buffers = 1 if self.samples > 1 else 0
        config.samples = self.samples
        # Find monitor

        # Open window
        self.window = PygletWrapper(
            width=self.width, height=self.height,
            caption=self.title,
            resizable=self.resizable,
            vsync=self.vsync,
            fullscreen=self.fullscreen,
        )
        self.window.set_mouse_visible(self.cursor)

        self.window.event(self.on_key_press)
        self.window.event(self.on_key_release)
        self.window.event(self.on_mouse_motion)
        self.window.event(self.on_resize)

        self.ctx = moderngl.create_context(require=self.gl_version.code)
        context.WINDOW = self
        self.fbo = self.ctx.screen
        self.set_default_viewport()

    def on_key_press(self, symbol, modifiers):
        """
        Pyglet specific key press callback.
        Forwards and translates the events to :py:func:`keyboard_event`
        """
        self.keyboard_event(symbol, self.keys.ACTION_PRESS, modifiers)

    def on_key_release(self, symbol, modifiers):
        """
        Pyglet specific key release callback.
        Forwards and translates the events to :py:func:`keyboard_event`
        """
        self.keyboard_event(symbol, self.keys.ACTION_RELEASE, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        """
        Pyglet specific mouse motion callback.
        Forwards and traslates the event to :py:func:`cursor_event`
        """
        # screen coordinates relative to the lower-left corner
        self.cursor_event(x, self.buffer_height - y, dx, dy)

    def on_resize(self, width, height):
        """
        Pyglet specific callback for window resize events.
        """
        self.width, self.height = width, height
        self.buffer_width, self.buffer_height = width, height
        self.resize(width, height)

    def use(self):
        """Render to this window"""
        self.fbo.use()

    def swap_buffers(self):
        """
        Swap buffers, increment frame counter and pull events
        """
        if not self.window.context:
            return

        self.frames += 1
        self.window.flip()
        self.window.dispatch_events()

    def should_close(self) -> bool:
        """
        returns the ``has_exit`` state in the pyglet window
        """
        return self.window.has_exit

    def close(self):
        """
        Sets the close state in the pyglet window
        """
        self.window.close()

    def terminate(self):
        """
        No cleanup is really needed. Empty method
        """
        pass


class PygletWrapper(pyglet.window.Window):
    """
    Block out some window methods so pyglet behaves
    """

    def on_resize(self, width, height):
        """For some reason pyglet calls its own resize handler randomly"""
        pass

    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        pass

    def on_draw(self):
        pass
