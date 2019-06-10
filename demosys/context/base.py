import sys
from collections import namedtuple
from typing import Tuple

import moderngl
import demosys
from demosys import project
from demosys.conf import settings
from demosys.view import screenshot

GLVersion = namedtuple('GLVersion', ['major', 'minor', 'code'])


class BaseKeys:
    """
    Namespace for generic key constants
    working across all window types.
    """
    ACTION_PRESS = 'ACTION_PRESS'
    ACTION_RELEASE = 'ACTION_RELEASE'


class BaseWindow:
    """
    The base window we extend when adding new window types to the system.
    """
    keys = None  #: The key class/namespace used by the window defining keyboard constants

    def __init__(self):
        """
        Base window intializer reading values from ``settings``.

        When creating the initializer in your own window always call
        this methods using ``super().__init__()``.

        The main responsebility of the initializer is to:

        * initialize the window library
        * identify the window framebuffer
        * set up keyboard and mouse events
        * create the ``moderngl.Context`` instance
        * register the window in ``context.WINDOW``
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
    def size(self) -> Tuple[int, int]:
        """
        (width, height) tuple containing the window size.

        Note that for certain displays we rely on :py:func:`buffer_size`
        to get the actual window buffer size. This is fairly common
        for retina and 4k displays where the UI scale is > 1.0
        """
        return (self.width, self.height)

    @property
    def buffer_size(self) -> Tuple[int, int]:
        """
        (width, heigh) buffer size of the window.

        This is the actual buffer size of the window
        taking UI scale into account. A 1920 x 1080
        window running in an environment with UI scale 2.0
        would have a 3840 x 2160 window buffer.
        """
        return (self.buffer_width, self.buffer_height)

    def draw(self, current_time, frame_time):
        """
        Draws a frame. Internally it calls the
        configured timeline's draw method.

        Args:
            current_time (float): The current time (preferrably always from the configured timer class)
            frame_time (float): The duration of the previous frame in seconds
        """
        self.set_default_viewport()
        self.timeline.draw(current_time, frame_time, self.fbo)

    def clear(self):
        """
        Clear the window buffer
        """
        self.ctx.fbo.clear(
            red=self.clear_color[0],
            green=self.clear_color[1],
            blue=self.clear_color[2],
            alpha=self.clear_color[3],
            depth=self.clear_depth,
        )

    def clear_values(self, red=0.0, green=0.0, blue=0.0, alpha=0.0, depth=1.0):
        """
        Sets the clear values for the window buffer.

        Args:
            red (float): red compoent
            green (float): green compoent
            blue (float): blue compoent
            alpha (float): alpha compoent
            depth (float): depth value
        """
        self.clear_color = (red, green, blue, alpha)
        self.clear_depth = depth

    def use(self):
        """
        Set the window buffer as the current render target

        Raises:
            NotImplementedError
        """
        raise NotImplementedError("Window.use() not implemented in window class {}".format(self.__class__))

    def swap_buffers(self):
        """
        Swap the buffers. Most windows have at least support for double buffering
        cycling a back and front buffer.

        Raises:
            NotImplementedError
        """
        raise NotImplementedError()

    def resize(self, width, height):
        """
        Resize the window. Should normallty be overriden
        when implementing a window as most window libraries need additional logic here.

        Args:
            width (int): Width of the window
            height: (int): Height of the window
        """
        self.set_default_viewport()

    def close(self):
        """
        Set the window in close state. This doesn't actually close the window,
        but should make :py:func:`should_close` return ``True`` so the
        main loop can exit gracefully.

        Raises:
            NotImplementedError
        """
        raise NotImplementedError()

    def should_close(self) -> bool:
        """
        Check if window should close. This should always be checked in the main draw loop.

        Raises:
            NotImplementedError
        """
        raise NotImplementedError()

    def terminate(self):
        """
        The actual teardown of the window.

        Raises:
            NotImplementedError
        """
        raise NotImplementedError()

    def keyboard_event(self, key, action, modifier):
        """
        Handles the standard keyboard events such as camera movements,
        taking a screenshot, closing the window etc.

        Can be overriden add new keyboard events. Ensure this method
        is also called if you want to keep the standard features.

        Arguments:
            key: The key that was pressed or released
            action: The key action. Can be `ACTION_PRESS` or `ACTION_RELEASE`
            modifier: Modifiers such as holding shift or ctrl
        """
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
        """
        The standard mouse movement event method.
        Can be overriden to add new functionality.
        By default this feeds the system camera with new values.

        Args:
            x: The current mouse x position
            y: The current mouse y position
            dx: Delta x postion (x position difference from the previous event)
            dy: Delta y postion (y position difference from the previous event)
        """
        self.sys_camera.rot_state(x, y)

    def print_context_info(self):
        """
        Prints moderngl context info.
        """
        print()
        print("Version Info")
        print("------------")
        print("demosys-py :", demosys.__version__)
        print('ModernGL   :', moderngl.__version__)
        print('vendor     :', self.ctx.info['GL_VENDOR'])
        print('renderer   :', self.ctx.info['GL_RENDERER'])
        print('version    :', self.ctx.info['GL_VERSION'])
        print('code       :', self.ctx.version_code)
        print('python     :', sys.version)
        print('platform   :', sys.platform)
        print()

    def set_default_viewport(self):
        """
        Calculates the viewport based on the configured aspect ratio in settings.
        Will add black borders if the window do not match the viewport.
        """
        # The expected height with the current viewport width
        expected_height = int(self.buffer_width / self.aspect_ratio)

        # How much positive or negative y padding
        blank_space = self.buffer_height - expected_height
        self.fbo.viewport = (0, blank_space // 2, self.buffer_width, expected_height)
