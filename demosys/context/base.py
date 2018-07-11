import sys
from collections import namedtuple

import moderngl as mgl
from demosys.conf import settings

GLVersion = namedtuple('GLVersion', ['major', 'minor'])


class Window:

    def __init__(self):
        """
        Base window intializer

        :param width: window width
        :param height: window height
        """
        self.width = settings.WINDOW['size'][0]
        self.height = settings.WINDOW['size'][1]

        self.buffer_width = self.width
        self.buffer_height = self.height

        self.fbo = None
        self.sys_camera = None
        self.timer = None
        self.resources = None

        self.gl_version = GLVersion(*settings.OPENGL['version'])
        self.resizable = settings.WINDOW.get('resizable') or False
        self.title = settings.WINDOW.get('title') or "demosys-py"
        self.aspect_ratio = settings.WINDOW.get('aspect_ratio', 16 / 9)

        self.resizable = settings.WINDOW.get('resizable')
        self.fullscreen = settings.WINDOW.get('fullscreen')
        self.vsync = settings.WINDOW.get('vsync')
        self.cursor = settings.WINDOW.get('cursor')

        # ModernGL context
        self.ctx = None

    def clear(self):
        """Clear the scren"""
        self.ctx.clear(
            red=0.0, blue=0.0, green=0.0, alpha=0.0, depth=1.0,
            viewport=(0, 0, self.buffer_width, self.buffer_height)
        )

    def viewport(self):
        self.fbo.use()

    def swap_buffers(self):
        """Swap frame buffer"""
        raise NotImplementedError()

    def resize(self, width, height):
        """Resize window"""
        raise NotImplementedError()

    def close(self):
        """Set the close state"""
        raise NotImplementedError()

    def should_close(self):
        """Check if window should close"""
        raise NotImplementedError()

    def terminate(self):
        """Cleanup after close"""
        raise NotImplementedError()

    def print_context_info(self):
        """Prints out context info"""
        print("Context Version:")
        print('ModernGL:', mgl.__version__)
        print('vendor:', self.ctx.info['GL_VENDOR'])
        print('renderer:', self.ctx.info['GL_RENDERER'])
        print('version:', self.ctx.info['GL_VERSION'])
        print('python:', sys.version)
        print('platform:', sys.platform)
        print('code:', self.ctx.version_code)
