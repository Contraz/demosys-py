"""
Quick and dirty controller to get things up and running.
Thins needs to be improved once more pieces fall in place.
"""
from OpenGL import GL
import glfw
from demosys.view.window import Window
from demosys.effects.registry import Effect
from demosys.opengl import fbo
from demosys.opengl.fbo import WINDOW_FBO
from demosys import resources
from demosys.conf import settings
from demosys.scene import camera
from demosys.utils import module_loading
from . import screenshot

WINDOW = None
TIMER = None
CAMERA = None


def run(manager=None):
    """Initialize, load and run"""
    global WINDOW
    WINDOW = Window()
    fbo.WINDOW = WINDOW

    print("Loader started at", glfw.get_time())

    # Inject attributes into the base Effect class
    Effect.window_width = WINDOW.buffer_width
    Effect.window_height = WINDOW.buffer_height
    Effect.window_aspect = WINDOW.width / WINDOW.height

    # Set up the default system camera
    global CAMERA
    CAMERA = camera.Camera(aspect=Effect.window_aspect, fov=60.0, near=1, far=1000)
    Effect.sys_camera = CAMERA

    # Initialize Effects
    if not manager.pre_load():
        return

    # Load resources
    num_resources = resources.count()
    print("Loading {} resources".format(num_resources))
    resources.load()

    # Post-Load actions for effects
    if not manager.post_load():
        return

    glfw.set_key_callback(WINDOW.window, key_event_callback)
    glfw.set_cursor_pos_callback(WINDOW.window, mouse_event_callback)
    glfw.set_window_size_callback(WINDOW.window, window_resize_callback)

    # Initialize timer
    global TIMER
    timer_cls = module_loading.import_string(settings.TIMER)
    TIMER = timer_cls(getattr(settings, 'ROCKET'))
    TIMER.start()

    frames, ft = 0, 0
    prev_time = TIMER.get_time()
    while not WINDOW.should_close():
        t = TIMER.get_time()
        GL.glViewport(0, 0, WINDOW.buffer_width, WINDOW.buffer_height)
        GL.glClearColor(0.0, 0.0, 0.0, 0.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT | GL.GL_STENCIL_BUFFER_BIT)

        manager.draw(t, ft, WINDOW_FBO)

        WINDOW.swap_buffers()
        WINDOW.poll_events()
        frames += 1
        ft = t - prev_time
        prev_time = t

    duration = TIMER.stop()
    if duration > 0:
        fps = round(frames / duration, 2)
        print("Duration: {}s rendering {} frames at {} fps".format(duration, frames, fps))

    WINDOW.terminate()


def key_event_callback(window, key, scancode, action, mods):
    """
    :param window: Window event origin
    :param key: The keyboard key that was pressed or released.
    :param scancode: The system-specific scancode of the key.
    :param action: GLFW_PRESS, GLFW_RELEASE or GLFW_REPEAT
    :param mods: Bit field describing which modifier keys were held down.
    """
    # print("Key event:", key, scancode, action, mods)

    # The well-known standard key for quick exit
    if key == glfw.KEY_ESCAPE:
        WINDOW.set_should_close()

    # Toggle pause time
    elif key == glfw.KEY_SPACE and action == glfw.PRESS:
        TIMER.toggle_pause()

    # Camera movement
    # Right
    if key == glfw.KEY_D:
        if action == glfw.PRESS:
            CAMERA.move_state(camera.RIGHT, True)
        elif action == glfw.RELEASE:
            CAMERA.move_state(camera.RIGHT, False)
    # Left
    elif key == glfw.KEY_A:
        if action == glfw.PRESS:
            CAMERA.move_state(camera.LEFT, True)
        elif action == glfw.RELEASE:
            CAMERA.move_state(camera.LEFT, False)
    # Forward
    elif key == glfw.KEY_W:
        if action == glfw.PRESS:
            CAMERA.move_state(camera.FORWARD, True)
        if action == glfw.RELEASE:
            CAMERA.move_state(camera.FORWARD, False)
    # Backwards
    elif key == glfw.KEY_S:
        if action == glfw.PRESS:
            CAMERA.move_state(camera.BACKWARD, True)
        if action == glfw.RELEASE:
            CAMERA.move_state(camera.BACKWARD, False)

    # UP
    elif key == glfw.KEY_Q:
        if action == glfw.PRESS:
            CAMERA.move_state(camera.UP, True)
        if action == glfw.RELEASE:
            CAMERA.move_state(camera.UP, False)

    # Down
    elif key == glfw.KEY_E:
        if action == glfw.PRESS:
            CAMERA.move_state(camera.DOWN, True)
        if action == glfw.RELEASE:
            CAMERA.move_state(camera.DOWN, False)

    # Screenshots
    if key == glfw.KEY_X and action == glfw.PRESS:
        screenshot.create()


def mouse_event_callback(window, x, y):
    CAMERA.rot_state(x, y)


def window_resize_callback(window, width, height):
    WINDOW.resize(width, height)
