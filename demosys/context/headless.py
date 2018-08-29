import moderngl
from demosys import context
from demosys.conf import ImproperlyConfigured, settings

from .base import BaseWindow


class Window(BaseWindow):
    """
    Headless window using a standalone ``moderngl.Context``.
    """
    def __init__(self):
        """
        Creates a standalone ``moderngl.Context``.
        The headless window currently have no event input from keyboard or mouse.

        Using this window require either ``settings`` values to be present:

        * ``HEADLESS_FRAMES``: How many frames should be rendered before closing the window
        * ``HEADLESS_DURATION``: How many seconds rendering should last before the window closes

        """
        super().__init__()

        self.headless_frames = getattr(settings, 'HEADLESS_FRAMES', 0)
        self.headless_duration = getattr(settings, 'HEADLESS_DURATION', 0)

        if not self.headless_frames and not self.headless_duration:
            raise ImproperlyConfigured("HEADLESS_DURATION or HEADLESS_FRAMES not present in settings")

        self._close = False
        self.ctx = moderngl.create_standalone_context(require=self.gl_version.code)
        context.WINDOW = self

        self.fbo = self.ctx.framebuffer(
            color_attachments=self.ctx.texture(self.size, 4),
            depth_attachment=self.ctx.depth_texture(self.size),
        )

        self.set_default_viewport()
        self.fbo.use()

    def draw(self, current_time, frame_time):
        """
        Calls the superclass ``draw()`` methods and checks ``HEADLESS_FRAMES``/``HEADLESS_DURATION``
        """
        super().draw(current_time, frame_time)

        if self.headless_duration and current_time >= self.headless_duration:
            self.close()

    def use(self):
        """
        Binds the framebuffer representing this window
        """
        self.fbo.use()

    def should_close(self) -> bool:
        """Checks if the internal close state is set"""
        return self._close

    def close(self):
        """Sets the internal close state"""
        self._close = True

    def resize(self, width, height):
        """
        Resizing is not supported by the headless window.
        We simply override with an empty method.
        """
        pass

    def swap_buffers(self):
        """
        Headless window currently don't support double buffering.
        We only increment the frame counter here.
        """
        self.frames += 1

        if self.headless_frames and self.frames >= self.headless_frames:
            self.close()

    def terminate(self):
        """
        No teardown is needed. We override with an empty method
        """
        pass
