import glfw

import moderngl
from demosys.scene import camera
from demosys.view import screenshot
from demosys.opengl import FBO
from demosys import context
from .base import Window


class GLFW_Window(Window):
    min_glfw_version = (3, 2, 1)

    def __init__(self):
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
        self.fbo = FBO()
        self.fbo.ctx = self.ctx
        self.fbo.fbo = self.ctx.screen
        self.fbo.default_framebuffer = True
        self.set_default_viewport()

    def use(self):
        self.ctx.screen.use()

    def should_close(self):
        return glfw.window_should_close(self.window)

    def close(self):
        glfw.set_window_should_close(self.window, True)

    def swap_buffers(self):
        self.frames += 1
        glfw.swap_buffers(self.window)
        self.poll_events()

    def resize(self, width, height):
        self.width = width
        self.height = height
        self.buffer_width, self.buffer_height = glfw.get_framebuffer_size(self.window)
        print("Resize:", self.width, self.height, self.buffer_width, self.buffer_height)
        super().resize(width, height)

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

    def key_event_callback(self, window, key, scancode, action, mods):
        """
        Key event callback for glfw

        :param window: Window event origin
        :param key: The keyboard key that was pressed or released.
        :param scancode: The system-specific scancode of the key.
        :param action: GLFW_PRESS, GLFW_RELEASE or GLFW_REPEAT
        :param mods: Bit field describing which modifier keys were held down.
        """
        # print("Key event:", key, scancode, action, mods)

        # The well-known standard key for quick exit
        if key == glfw.KEY_ESCAPE:
            self.close()
            return

        # Toggle pause time
        if key == glfw.KEY_SPACE and action == glfw.PRESS:
            self.timer.toggle_pause()

        # Camera movement
        # Right
        if key == glfw.KEY_D:
            if action == glfw.PRESS:
                self.sys_camera.move_state(camera.RIGHT, True)
            elif action == glfw.RELEASE:
                self.sys_camera.move_state(camera.RIGHT, False)
        # Left
        elif key == glfw.KEY_A:
            if action == glfw.PRESS:
                self.sys_camera.move_state(camera.LEFT, True)
            elif action == glfw.RELEASE:
                self.sys_camera.move_state(camera.LEFT, False)
        # Forward
        elif key == glfw.KEY_W:
            if action == glfw.PRESS:
                self.sys_camera.move_state(camera.FORWARD, True)
            if action == glfw.RELEASE:
                self.sys_camera.move_state(camera.FORWARD, False)
        # Backwards
        elif key == glfw.KEY_S:
            if action == glfw.PRESS:
                self.sys_camera.move_state(camera.BACKWARD, True)
            if action == glfw.RELEASE:
                self.sys_camera.move_state(camera.BACKWARD, False)

        # UP
        elif key == glfw.KEY_Q:
            if action == glfw.PRESS:
                self.sys_camera.move_state(camera.UP, True)
            if action == glfw.RELEASE:
                self.sys_camera.move_state(camera.UP, False)

        # Down
        elif key == glfw.KEY_E:
            if action == glfw.PRESS:
                self.sys_camera.move_state(camera.DOWN, True)
            if action == glfw.RELEASE:
                self.sys_camera.move_state(camera.DOWN, False)

        # Screenshots
        if key == glfw.KEY_X and action == glfw.PRESS:
            screenshot.create()

        if key == glfw.KEY_R and action == glfw.PRESS:
            self.resources.shaders.reload()

        # Forward the event to the effect manager
        self.manager.key_event(key, scancode, action, mods)

    def mouse_event_callback(self, window, xpos, ypos):
        """
        Mouse event callback from glfw

        :param window: The window
        :param xpos: viewport x pos
        :param ypos: viewport y pos
        """
        self.sys_camera.rot_state(xpos, ypos)

    def window_resize_callback(self, window, width, height):
        """
        Window resize callback for glfw

        :param window: The window
        :param width: New width
        :param height: New height
        """
        print("Resize", width, height)
        self.resize(width, height)
