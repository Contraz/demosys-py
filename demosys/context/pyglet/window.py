import pyglet

import moderngl
from demosys import context
from demosys.context.base import BaseWindow
from .keys import Keys


class Window(BaseWindow):
    keys = Keys

    def __init__(self):
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
        self.window = pyglet.window.Window(
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
        self.keyboard_event(symbol, self.keys.ACTION_PRESS, modifiers)

    def on_key_release(self, symbol, modifiers):
        self.keyboard_event(symbol, self.keys.ACTION_RELEASE, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        # screen coordinates relative to the lower-left corner
        self.cursor_event(x, self.buffer_height - y, dx, dy)

    def on_resize(self, width, height):
        self.width, self.height = width, height
        self.buffer_width, self.buffer_height = width, height
        self.resize(width, height)

    def use(self):
        """Render to this window"""
        self.fbo.use()

    def swap_buffers(self):
        self.frames += 1
        self.window.flip()
        self.window.dispatch_events()

    def should_close(self):
        return self.window.has_exit

    def close(self):
        self.window.close()

    def terminate(self):
        pass
