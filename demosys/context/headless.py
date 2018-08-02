import moderngl
from demosys import context
from demosys.conf import ImproperlyConfigured, settings
from demosys.opengl.fbo import FBO

from .base import Window


class HeadlessWindow(Window):

    def __init__(self):
        super().__init__()

        self.headless_frames = getattr(settings, 'HEADLESS_FRAMES', 0)
        self.headless_duration = getattr(settings, 'HEADLESS_DURATION', 0)

        if not self.headless_frames and not self.headless_duration:
            raise ImproperlyConfigured("HEADLESS_DURATION or HEADLESS_FRAMES not present in settings")

        self._close = False
        self.ctx = moderngl.create_standalone_context(require=self.gl_version.code)
        context.WINDOW = self

        self.fbo = FBO()
        self.fbo.ctx = self.ctx
        self.fbo.fbo = self.ctx.framebuffer(
            color_attachments=self.ctx.texture((self.width, self.height), 4),
            depth_attachment=self.ctx.depth_texture((self.width, self.height)),
        )
        self.fbo.default_framebuffer = True
        self.set_default_viewport()

    def draw(self, current_time, frame_time):
        super().draw(current_time, frame_time)

        if self.headless_duration and current_time >= self.headless_duration:
            self.close()

    def use(self):
        self.fbo.use(stack=False)

    def should_close(self):
        return self._close

    def close(self):
        self._close = True

    def resize(self, width, height):
        pass

    def swap_buffers(self):
        self.frames += 1

        if self.headless_frames and self.frames >= self.headless_frames:
            self.close()

    def terminate(self):
        pass

    def mgl_fbo(self):
        return self.screenbuffer.mglo
