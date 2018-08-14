import sys
from collections import namedtuple

import moderngl
from demosys import project
from demosys.conf import settings
from demosys.view import screenshot

GLVersion = namedtuple('GLVersion', ['major', 'minor', 'code'])


class BaseKeys:
    """Generic constants here"""
    ACTION_PRESS = 'ACTION_PRESS'
    ACTION_RELEASE = 'ACTION_RELEASE'


class BaseWindow:
    keys = None

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
        self.timeline = None

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

    @property
    def size(self):
        return (self.width, self.height)

    @property
    def buffer_size(self):
        return (self.buffer_width, self.buffer_height)

    def draw(self, current_time, frame_time):
        self.set_default_viewport()
        self.timeline.draw(current_time, frame_time, self.fbo)

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

    def keyboard_event(self, key, action, modifier):
        # The well-known standard key for quick exit
        if key == self.keys.ESCAPE:
            self.close()
            return

        # Toggle pause time
        if key == self.keys.SPACE and action == self.keys.ACTION_PRESS:
            self.timer.toggle_pause()

        # Camera movement
        # Right
        if key == self.keys.D:
            if action == self.keys.ACTION_PRESS:
                self.sys_camera.move_right(True)
            elif action == self.keys.ACTION_RELEASE:
                self.sys_camera.move_right(False)
        # Left
        elif key == self.keys.A:
            if action == self.keys.ACTION_PRESS:
                self.sys_camera.move_left(True)
            elif action == self.keys.ACTION_RELEASE:
                self.sys_camera.move_left(False)
        # Forward
        elif key == self.keys.W:
            if action == self.keys.ACTION_PRESS:
                self.sys_camera.move_forward(True)
            if action == self.keys.ACTION_RELEASE:
                self.sys_camera.move_forward(False)
        # Backwards
        elif key == self.keys.S:
            if action == self.keys.ACTION_PRESS:
                self.sys_camera.move_backward(True)
            if action == self.keys.ACTION_RELEASE:
                self.sys_camera.move_backward(False)

        # UP
        elif key == self.keys.Q:
            if action == self.keys.ACTION_PRESS:
                self.sys_camera.move_down(True)
            if action == self.keys.ACTION_RELEASE:
                self.sys_camera.move_down(False)

        # Down
        elif key == self.keys.E:
            if action == self.keys.ACTION_PRESS:
                self.sys_camera.move_up(True)
            if action == self.keys.ACTION_RELEASE:
                self.sys_camera.move_up(False)

        # Screenshots
        if key == self.keys.X and action == self.keys.ACTION_PRESS:
            screenshot.create()

        if key == self.keys.R and action == self.keys.ACTION_PRESS:
            project.instance.reload_programs()

        if key == self.keys.RIGHT and action == self.keys.ACTION_PRESS:
            self.timer.set_time(self.timer.get_time() + 10.0)

        if key == self.keys.LEFT and action == self.keys.ACTION_PRESS:
            self.timer.set_time(self.timer.get_time() - 10.0)

        # Forward the event to the timeline
        self.timeline.key_event(key, action, modifier)

    def cursor_event(self, x, y, dx, dy):
        self.sys_camera.rot_state(x, y)

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
