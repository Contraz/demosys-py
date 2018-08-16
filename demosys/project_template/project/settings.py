"""
Auto generated settings file for project $project_name
"""

import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SCREENSHOT_PATH = os.path.join(PROJECT_DIR, 'screenshots')

# OpenGL context configuration
# version: (MAJOR, MINOR)
OPENGL = {
    "version": (3, 3),
}

# Window / context properties
WINDOW = {
    "class": "demosys.context.pyqt.Window",
    "size": (1280, 720),
    "aspect_ratio": 16 / 9,
    "fullscreen": False,
    "resizable": True,
    "title": "demosys-py",
    "vsync": True,
    "cursor": True,
    "samples": 0,
}

MUSIC = None

TIMER = 'demosys.timers.clock.Timer'

TIMELINE = 'demosys.timeline.single.Timeline'

PROJECT = "$project_name.project.Project"

ROCKET = {
    'mode': 'editor',
    'rps': 24,
    'project': None,
    'files': None,
}

PROGRAM_DIRS = ()

TEXTURE_DIRS = ()

SCENE_DIRS = ()

DATA_DIRS = ()
