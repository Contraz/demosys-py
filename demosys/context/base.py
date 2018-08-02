import sys
from collections import namedtuple

import moderngl
from demosys.conf import settings

GLVersion = namedtuple('GLVersion', ['major', 'minor', 'code'])


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

        self.gl_version = GLVersion(
            *settings.OPENGL['version'],
            int("{}{}0".format(*settings.OPENGL['version']))
        )
        self.title = settings.WINDOW.get('title') or "demosys-py"
        self.aspect_ratio = settings.WINDOW.get('aspect_ratio', 16 / 9)
        self.samples = settings.WINDOW.get('samples', 0)

        self.resizable = settings.WINDOW.get('resizable') or False
        self.fullscreen = settings.WINDOW.get('fullscreen')
        self.vsync = settings.WINDOW.get('vsync')
        self.cursor = settings.WINDOW.get('cursor')

        self.clear_color = (0.0, 0.0, 0.0, 0.0)
        self.clear_depth = (1.0)

        # ModernGL context
        self.ctx = None

    def draw(self, current_time, frame_time):
        self.set_default_viewport()
        self.manager.draw(current_time, frame_time, self.fbo)

    def clear(self):
        """Clear the scren"""
        self.ctx.fbo.clear(
            red=self.clear_color[0],
            green=self.clear_color[1],
            blue=self.clear_color[2],
            alpha=self.clear_color[3],
            depth=self.clear_depth,
        )

    def clear_values(self, red=0.0, green=0.0, blue=0.0, alpha=0.0, depth=1.0):
        self.clear_color = (red, green, blue, alpha)
        self.clear_depth = depth

    def use(self):
        """Render to this window"""
        raise NotImplementedError()

    def swap_buffers(self):
        """Swap frame buffer"""
        raise NotImplementedError()

    def resize(self, width, height):
        """Resize window"""
        self.set_default_viewport()

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
        return self.ctx.screen

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

    def set_default_viewport(self):
        """Calculate viewport with correct aspect ratio"""
        # The expected height with the current viewport width
        expected_height = int(self.buffer_width / self.aspect_ratio)

        # How much positive or negative y padding
        blank_space = self.buffer_height - expected_height
        self.fbo.viewport = (0, blank_space // 2, self.buffer_width, expected_height)
