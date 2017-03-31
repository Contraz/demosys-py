"""
Quick and dirty controller to get things up and running.
Thins needs to be improved once more pieces fall in place.
"""
from OpenGL import GL
import glfw
from demosys.view.window import Window
from demosys.effects.registry import effects, Effect
from demosys.opengl import fbo
from demosys.opengl.fbo import WINDOW_FBO
from demosys import resources
from demosys.timeline import timers
from demosys.conf import settings
from demosys.scene.camera import Camera

WINDOW = None
TIMER = None
CAMERA = None


def run(runeffect=None):
    """Initialize, load and run"""
    global WINDOW
    WINDOW = Window()
    fbo.WINDOW = WINDOW

    print("Loader started at", glfw.get_time())
    # Inject attributes into the base Effect class
    Effect.window_width = WINDOW.buffer_width
    Effect.window_height = WINDOW.buffer_height
    Effect.window_aspect = WINDOW.width / WINDOW.height
    global CAMERA
    CAMERA = Camera(aspect=Effect.window_aspect, fov=60.0, near=1, far=1000)
    Effect.sys_camera = CAMERA

    # Initialize effects first so resources are registered
    effect_list = [cls for cls in effects.get_effects()]
    active_effect = None
    for effect in effect_list:
        effect.init()
        if effect.name == runeffect:
            active_effect = effect

    if not active_effect:
        print(f"Cannot find effect '{runeffect}'")
        print("Available effects:")
        print("\n".join(e.name for e in effect_list))
        return

    num_resources = resources.count()
    print(f"Loading {num_resources } resources")
    resources.load()

    glfw.set_key_callback(WINDOW.window, key_event_callback)

    global TIMER
    if settings.MUSIC:
        TIMER = timers.MusicTimer(source=settings.MUSIC)
    else:
        TIMER = timers.Timer()
    TIMER.start()

    frames = 0
    while not WINDOW.should_close():
        t = TIMER.get_time()
        GL.glViewport(0, 0, WINDOW.buffer_width, WINDOW.buffer_height)
        GL.glClearColor(0.0, 0.0, 0.0, 0.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT | GL.GL_STENCIL_BUFFER_BIT)

        active_effect.draw(t, WINDOW_FBO)

        WINDOW.swap_buffers()
        WINDOW.poll_events()
        frames += 1

    duration = TIMER.stop()
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
    if key == glfw.KEY_SPACE and action == glfw.PRESS:
        TIMER.toggle_pause()

