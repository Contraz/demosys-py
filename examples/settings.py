import os
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

SCREENSHOT_PATH = None

OPENGL = {
    "version": (3, 3),
}

WINDOW = {
    "class": "demosys.context.pyglet.Window",
    "size": (1280, 720),
    "aspect_ratio": 16 / 9,
    "fullscreen": False,
    "resizable": True,
    "title": "Examples",
    "vsync": True,
    "cursor": False,
    "samples": 4,
}

HEADLESS_DURATION = 100.0

ROCKET = {
    "mode": "editor",
    "rps": 24,
    "project": None,
    "files": None,
}
