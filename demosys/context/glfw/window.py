import glfw

import moderngl
from demosys import context
from demosys.context.base import BaseWindow
from demosys.context.glfw.keys import Keys


class Window(BaseWindow):
    """
    Window implementation using pyGLFW
    """
    min_glfw_version = (3, 2, 1)  #: The minimum glfw version required
    keys = Keys

    def __init__(self):
        """
        Initializes glfw, sets up key and mouse events and
        creates a ``moderngl.Context`` using the context glfw createad.

        Using the glfw window requires glfw binaries and pyGLFW.
        """
        super().__init__()

        if not glfw.init():
            raise ValueError("Failed to initialize glfw")

        self.check_glfw_version()

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, self.gl_version.major)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, self.gl_version.minor)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)
        glfw.window_hint(glfw.RESIZABLE, self.resizable)
        glfw.window_hint(glfw.DOUBLEBUFFER, True)
        glfw.window_hint(glfw.DEPTH_BITS, 24)
        glfw.window_hint(glfw.SAMPLES, self.samples)

        monitor = None
        if self.fullscreen:
            # Use the primary monitors current resolution
            monitor = glfw.get_primary_monitor()
            mode = glfw.get_video_mode(monitor)

            self.width, self.height = mode.size.width, mode.size.height
            print("picked fullscreen mode:", mode)

        print("Window size:", self.width, self.height)
        self.window = glfw.create_window(self.width, self.height, self.title, monitor, None)

        if not self.window:
            glfw.terminate()
            raise ValueError("Failed to create window")

        if not self.cursor:
            glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_DISABLED)

        # Get the actual buffer size of the window
        # This is important for some displays like Apple's Retina as reported window sizes are virtual
        self.buffer_width, self.buffer_height = glfw.get_framebuffer_size(self.window)
        print("Frame buffer size:", self.buffer_width, self.buffer_height)
        print("Actual window size:", glfw.get_window_size(self.window))

        glfw.make_context_current(self.window)

        # The number of screen updates to wait from the time glfwSwapBuffers
        # was called before swapping the buffers and returning
        if self.vsync:
            glfw.swap_interval(1)

        glfw.set_key_callback(self.window, self.key_event_callback)
        glfw.set_cursor_pos_callback(self.window, self.mouse_event_callback)
        glfw.set_window_size_callback(self.window, self.window_resize_callback)

        # Create mederngl context from existing context
        self.ctx = moderngl.create_context(require=self.gl_version.code)
        context.WINDOW = self
        self.fbo = self.ctx.screen
        self.set_default_viewport()

    def use(self):
        """
        Bind the window framebuffer making it the current render target
        """
        self.fbo.use()

    def should_close(self):
        """
        Ask glfw is the window should be closed
        """
        return glfw.window_should_close(self.window)

    def close(self):
        """
        Set the window closing state in glfw
        """
        glfw.set_window_should_close(self.window, True)

    def swap_buffers(self):
        """
        Swaps buffers, incement the framecounter and pull events.
        """
        self.frames += 1
        glfw.swap_buffers(self.window)
        self.poll_events()

    def resize(self, width, height):
        """
        Sets the new size and buffer size internally
        """
        self.width = width
        self.height = height
        self.buffer_width, self.buffer_height = glfw.get_framebuffer_size(self.window)
        self.set_default_viewport()

    def terminate(self):
        """
        Terminates the glfw library
        """
        glfw.terminate()

    def poll_events(self):
        """Poll events from glfw"""
        glfw.poll_events()

    def check_glfw_version(self):
        """
        Ensure glfw library  version is compatible
        """
        print("glfw version: {} (python wrapper version {})".format(glfw.get_version(), glfw.__version__))
        if glfw.get_version() < self.min_glfw_version:
            raise ValueError("Please update glfw binaries to version {} or later".format(self.min_glfw_version))

    def key_event_callback(self, window, key, scancode, action, mods):
        """
        Key event callback for glfw.
        Translates and forwards keyboard event to :py:func:`keyboard_event`

        :param window: Window event origin
        :param key: The key that was pressed or released.
        :param scancode: The system-specific scancode of the key.
        :param action: GLFW_PRESS, GLFW_RELEASE or GLFW_REPEAT
        :param mods: Bit field describing which modifier keys were held down.
        """
        self.keyboard_event(key, action, mods)

    def mouse_event_callback(self, window, xpos, ypos):
        """
        Mouse event callback from glfw.
        Translates the events forwarding them to :py:func:`cursor_event`.

        :param window: The window
        :param xpos: viewport x pos
        :param ypos: viewport y pos
        """
        # screen coordinates relative to the top-left corner
        self.cursor_event(xpos, ypos, 0, 0)

    def window_resize_callback(self, window, width, height):
        """
        Window resize callback for glfw

        :param window: The window
        :param width: New width
        :param height: New height
        """
        self.resize(width, height)
