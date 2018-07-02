"""
Quick and dirty controller to get things up and running.
Thins needs to be improved once more pieces fall in place.
"""
import glfw
import OpenGL

from demosys.context.glfw import GLTFWindow
from demosys.effects.registry import Effect
from demosys.opengl import fbo
from demosys import resources
from demosys.conf import settings
from demosys.scene import camera
from demosys.utils import module_loading
from demosys import context
from . import screenshot

# We still use PyOpenGL for samplers and don't want it to halt on errors
OpenGL.ERROR_CHECKING = False

TIMER = None
CAMERA = None
MANAGER = None


def run(manager=None):
    """
    Initialize, load and run

    :param manager: The effect manager to use
    """
    global MANAGER
    MANAGER = manager

    context.WINDOW = GLTFWindow()

    fbo.WINDOW_FBO = fbo.WindowFBO(context.WINDOW)

    print("Loader started at", glfw.get_time())

    # Inject attributes into the base Effect class
    Effect.window_width = context.WINDOW.buffer_width
    Effect.window_height = context.WINDOW.buffer_height
    Effect.window_aspect = context.WINDOW.aspect_ratio
    Effect.ctx = context.ctx()

    # Set up the default system camera
    global CAMERA
    CAMERA = camera.SystemCamera(aspect=context.WINDOW.aspect_ratio, fov=60.0, near=1, far=1000)
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

    glfw.set_key_callback(context.WINDOW.window, key_event_callback)
    glfw.set_cursor_pos_callback(context.WINDOW.window, mouse_event_callback)
    glfw.set_window_size_callback(context.WINDOW.window, window_resize_callback)

    # Initialize timer
    global TIMER
    timer_cls = module_loading.import_string(settings.TIMER)
    TIMER = timer_cls()
    TIMER.start()

    # Main loop
    frames, frame_time = 0, 60.0 / 1000.0
    prev_time = TIMER.get_time()
    time_start = glfw.get_time()
    while not context.WINDOW.should_close():
        # Immediately get control of the current time
        current_time = TIMER.get_time()

        # Set the viewport as FBOs will change the values
        context.ctx().viewport = (0, 0, context.WINDOW.buffer_width, context.WINDOW.buffer_height)

        # Clear the buffer
        context.ctx().clear(
            red=0.0, blue=0.0, green=0.0, alpha=0.0, depth=1.0,
            viewport=(0, 0, context.WINDOW.buffer_width, context.WINDOW.buffer_height)
        )

        # Tell the manager to draw stuff
        manager.draw(current_time, frame_time, fbo.WINDOW_FBO)

        # Swap buffers and deal with events and statistics
        context.WINDOW.swap_buffers()
        context.WINDOW.poll_events()
        frames += 1
        frame_time = current_time - prev_time
        prev_time = current_time

    duration_timer = TIMER.stop()
    duration = glfw.get_time() - time_start

    if duration > 0:
        fps = round(frames / duration, 2)
        print("Duration: {}s rendering {} frames at {} fps".format(duration, frames, fps))
        print("Timeline duration:", duration_timer)

    # Let the window and context clean itself up


def key_event_callback(window, key, scancode, action, mods):
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
        context.WINDOW.close()
        return

    # Toggle pause time
    if key == glfw.KEY_SPACE and action == glfw.PRESS:
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

    if key == glfw.KEY_R and action == glfw.PRESS:
        resources.shaders.reload()

    # Forward the event to the effect manager
    MANAGER.key_event(key, scancode, action, mods)


def mouse_event_callback(window, xpos, ypos):
    """
    Mouse event callback from glfw

    :param window: The window
    :param xpos: viewport x pos
    :param ypos: viewport y pos
    """
    CAMERA.rot_state(xpos, ypos)


def window_resize_callback(window, width, height):
    """
    Window resize callback for glfw

    :param window: The window
    :param width: New width
    :param height: New height
    """
    print("Resize", width, height)
    context.WINDOW.resize(width, height)
