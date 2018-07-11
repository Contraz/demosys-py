"""
Quick and dirty controller to get things up and running.
Thins needs to be improved once more pieces fall in place.
"""
import time

# We still use PyOpenGL for samplers and don't want it to halt on errors
import OpenGL
OpenGL.ERROR_CHECKING = False  # noqa

from demosys import context, resources
from demosys.conf import settings
from demosys.context.glfw import GLTFWindow
from demosys.effects.registry import Effect
from demosys.opengl.fbo import WindowFBO
from demosys.scene import camera
from demosys.utils import module_loading


def run(manager=None):
    """
    Initialize, load and run

    :param manager: The effect manager to use
    """
    # Load context class here
    window = GLTFWindow()
    window.manager = manager
    context.WINDOW = window
    window.print_context_info()

    WindowFBO.window = window
    window.fbo = WindowFBO

    print("Loader started at", time.time())

    # Inject attributes into the base Effect class
    setattr(Effect, '_window_width', context.WINDOW.buffer_width)
    setattr(Effect, '_window_height', context.WINDOW.buffer_height)
    setattr(Effect, '_window_aspect', context.WINDOW.aspect_ratio)
    setattr(Effect, '_ctx', context.ctx())

    # Set up the default system camera
    window.sys_camera = camera.SystemCamera(aspect=context.WINDOW.aspect_ratio, fov=60.0, near=1, far=1000)
    setattr(Effect, '_sys_camera', window.sys_camera)

    # Initialize Effects
    if not manager.pre_load():
        return

    # Load resources
    num_resources = resources.count()
    print("Loading {} resources".format(num_resources))
    window.resources = resources
    resources.load()

    # Post-Load actions for effects
    if not manager.post_load():
        return

    # Initialize timer
    timer_cls = module_loading.import_string(settings.TIMER)
    window.timer = timer_cls()
    window.timer.start()

    # Main loop
    frames, frame_time = 0, 60.0 / 1000.0
    # time_start = glfw.get_time()
    time_start = time.time()
    prev_time = window.timer.get_time()

    while not window.should_close():
        current_time = window.timer.get_time()

        window.viewport()
        window.clear()

        manager.draw(current_time, frame_time, WindowFBO)

        window.swap_buffers()

        frames += 1
        frame_time = current_time - prev_time
        prev_time = current_time

    duration_timer = window.timer.stop()
    duration = time.time() - time_start

    window.terminate()

    if duration > 0:
        fps = round(frames / duration, 2)
        print("Duration: {}s rendering {} frames at {} fps".format(duration, frames, fps))
        print("Timeline duration:", duration_timer)
