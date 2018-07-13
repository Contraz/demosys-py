import sys
from collections import namedtuple

import moderngl
from demosys.conf import settings
from demosys.opengl.fbo import WindowFBO
from demosys import context

GLVersion = namedtuple('GLVersion', ['major', 'minor'])


class Window:

    def __init__(self):
        """
        Base window intializer
        """
        self.frames = 0
        self.width = settings.WINDOW['size'][0]
        self.height = settings.WINDOW['size'][1]

        self.buffer_width = self.width
        self.buffer_height = self.height

        self.fbo = None
        self.sys_camera = None
        self.timer = None
        self.resources = None
        self.manager = None

        self.gl_version = GLVersion(*settings.OPENGL['version'])
        self.resizable = settings.WINDOW.get('resizable') or False
        self.title = settings.WINDOW.get('title') or "demosys-py"
        self.aspect_ratio = settings.WINDOW.get('aspect_ratio', 16 / 9)

        self.resizable = settings.WINDOW.get('resizable')
        self.fullscreen = settings.WINDOW.get('fullscreen')
        self.vsync = settings.WINDOW.get('vsync')
        self.cursor = settings.WINDOW.get('cursor')

        self._calc_viewport()

        # ModernGL context
        self.ctx = None

        WindowFBO.window = self
        self.fbo = WindowFBO
        context.WINDOW = self

    def draw(self, current_time, frame_time):
        self.manager.draw(current_time, frame_time, WindowFBO)

    def clear(self):
        """Clear the scren"""
        self.ctx.clear(
            red=0.0, blue=0.0, green=0.0, alpha=0.0, depth=1.0,
            viewport=self._viewport,
        )

    def use(self):
        """Render to this window"""
        raise NotImplementedError()

    def viewport(self):
        self.ctx.viewport = self._viewport

    def swap_buffers(self):
        """Swap frame buffer"""
        raise NotImplementedError()

    def resize(self, width, height):
        """Resize window"""
        self._calc_viewport()

    def close(self):
        """Set the close state"""
        raise NotImplementedError()

    def should_close(self):
        """Check if window should close"""
        raise NotImplementedError()

    def terminate(self):
        """Cleanup after close"""
        raise NotImplementedError()

    def mgl_fbo(self):
        """Returns the ModernGL fbo used by this window"""
        raise NotImplementedError()

    def print_context_info(self):
        """Prints out context info"""
        print("Context Version:")
        print('ModernGL:', moderngl.__version__)
        print('vendor:', self.ctx.info['GL_VENDOR'])
        print('renderer:', self.ctx.info['GL_RENDERER'])
        print('version:', self.ctx.info['GL_VERSION'])
        print('python:', sys.version)
        print('platform:', sys.platform)
        print('code:', self.ctx.version_code)

    def _calc_viewport(self):
        """Calculate viewport with correct aspect ratio"""
        # The expected height with the current viewport width
        expected_height = int(self.buffer_width / self.aspect_ratio)

        # How much positive or negative y padding
        blank_space = self.buffer_height - expected_height
        self._viewport = (0, blank_space // 2, self.buffer_width, expected_height)
