import glfw
import moderngl

from OpenGL import GL

from demosys.conf import settings
from demosys.core.exceptions import ImproperlyConfigured
from .base import Context

PROFILES = {
    'any': glfw.OPENGL_ANY_PROFILE,
    'core': glfw.OPENGL_CORE_PROFILE,
    'compat': glfw.OPENGL_COMPAT_PROFILE,
}


class GLTFWindow(Context):
    min_glfw_version = (3, 2, 1)

    def __init__(self):
        super().__init__(
            width=settings.WINDOW['size'][0],
            height=settings.WINDOW['size'][1],
        )
        self.resizable = settings.WINDOW.get('resizable') or False
        self.title = settings.WINDOW.get('title') or "demosys-py"
        self.aspect_ratio = settings.WINDOW.get('aspect_ratio', 16 / 9)

        if not glfw.init():
            raise ValueError("Failed to initialize glfw")

        self.check_glfw_version()

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, settings.OPENGL['version'][0])
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, settings.OPENGL['version'][1])

        profile = PROFILES.get(settings.OPENGL['profile'])
        if not profile:
            raise ImproperlyConfigured("OPENGL profile {} not supported".format(profile))

        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        if settings.OPENGL.get('forward_compat'):
            glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)
        if not settings.WINDOW.get('resizable'):
            glfw.window_hint(glfw.RESIZABLE, GL.GL_FALSE)

        glfw.window_hint(glfw.DOUBLEBUFFER, GL.GL_TRUE)

        glfw.window_hint(glfw.RED_BITS, 8)
        glfw.window_hint(glfw.GREEN_BITS, 8)
        glfw.window_hint(glfw.BLUE_BITS, 8)
        glfw.window_hint(glfw.ALPHA_BITS, 8)

        glfw.window_hint(glfw.DEPTH_BITS, 24)
        glfw.window_hint(glfw.STENCIL_BITS, 8)

        monitor = None
        if settings.WINDOW.get('fullscreen'):
            # Use the primary monitors current resolution
            monitor = glfw.get_primary_monitor()
            mode = glfw.get_video_mode(monitor)

            self.width, self.height = mode.size.width, mode.size.height
            print("picked fullscreen mode:", mode)

            # modes = glfw.get_video_modes(monitor)
            # print("Supported fullscreen resolutions:")
            # print("\n".join(str(m) for m in modes))
            #
            # # Pick a mode close to the configured one
            # for mode in modes:
            #     if self.width <= mode[0][0]:
            #         self.width, self.height = mode[0]
            #         print("picked fullscreen mode:", mode)
            #         break

        print("Window size:", self.width, self.height)
        self.window = glfw.create_window(self.width, self.height, self.title, monitor, None)

        if not self.window:
            glfw.terminate()
            raise ValueError("Failed to create window")

        if not settings.WINDOW.get('cursor'):
            glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_DISABLED)

        # Get the actual buffer size of the window
        # This is important for some displays like Apple's Retina as reported window sizes are virtual
        self.buffer_width, self.buffer_height = glfw.get_framebuffer_size(self.window)
        print("Frame buffer size:", self.buffer_width, self.buffer_height)

        print("Actual window size:", glfw.get_window_size(self.window))

        glfw.make_context_current(self.window)
        print("Context Version:", GL.glGetString(GL.GL_VERSION).decode())

        # The number of screen updates to wait from the time glfwSwapBuffers
        # was called before swapping the buffers and returning
        if settings.WINDOW.get('vsync'):
            glfw.swap_interval(1)

        # Create mederngl context from existing context
        self.ctx = moderngl.create_context()

    def should_close(self):
        return glfw.window_should_close(self.window)

    def close(self):
        glfw.set_window_should_close(self.window, True)

    def swap_buffers(self):
        glfw.swap_buffers(self.window)

    def resize(self, width, height):
        self.width = width
        self.height = height
        self.buffer_width, self.buffer_height = glfw.get_framebuffer_size(self.window)
        print("Resize:", self.width, self.height, self.buffer_width, self.buffer_height)

    def terminate(self):
        glfw.terminate()

    def poll_events(self):
        """Poll events from glfw"""
        glfw.poll_events()

    def check_glfw_version(self):
        """Ensure glfw version is compatible"""
        print("glfw version: {} (python wrapper version {})".format(glfw.get_version(), glfw.__version__))
        if glfw.get_version() < self.min_glfw_version:
            raise ValueError("Please update glfw binaries to version {} or later".format(self.min_glfw_version))
