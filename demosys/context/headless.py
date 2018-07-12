import moderngl
from demosys.conf import settings
from demosys.conf import ImproperlyConfigured
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
        self.ctx = moderngl.create_standalone_context()
        self.screenbuffer = FBO.create((self.width, self.height), depth=True)

    def draw(self, current_time, frame_time):
        super().draw(current_time, frame_time)

        if self.headless_duration and current_time >= self.headless_duration:
            self.close()

    def use(self):
        self.screenbuffer.use(stack=False)

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
