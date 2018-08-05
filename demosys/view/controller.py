"""
Quick and dirty controller to get things up and running.
Thins needs to be improved once more pieces fall in place.
"""
import time

from demosys import resources
from demosys.conf import settings
from demosys.effects.registry import Effect
from demosys.scene import camera
from demosys.utils import module_loading
from demosys.opengl.texture import helper


def run(manager=None, window=None):
    """
    Initialize, load and run

    :param manager: The effect manager to use
    """
    window.manager = manager

    helper._init_texture2d_draw()
    helper._init_depth_texture_draw()

    print("Loader started at", time.time())

    # Inject attributes into the base Effect class
    setattr(Effect, '_window', window)
    setattr(Effect, '_ctx', window.ctx)

    # Set up the default system camera
    window.sys_camera = camera.SystemCamera(aspect=window.aspect_ratio, fov=60.0, near=1, far=1000)
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
    frame_time = 60.0 / 1000.0
    time_start = time.time()
    prev_time = window.timer.get_time()

    while not window.should_close():
        current_time = window.timer.get_time()

        window.use()
        window.clear()
        window.draw(current_time, frame_time)
        window.swap_buffers()

        frame_time = current_time - prev_time
        prev_time = current_time

    duration_timer = window.timer.stop()
    duration = time.time() - time_start

    window.terminate()

    if duration > 0:
        fps = round(window.frames / duration, 2)
        print("Duration: {}s rendering {} frames at {} fps".format(duration, window.frames, fps))
        print("Timeline duration:", duration_timer)
