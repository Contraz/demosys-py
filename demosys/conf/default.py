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
    "class": "demosys.context.pyqt.GLFW_Window",
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

ROCKET = {
    'mode': 'editor',
    'rps': 24,
    'project': None,
    'files': None,
}

PROGRAM_DIRS = (

)

PROGRAM_FINDERS = (
    "demosys.finders.program.FileSystemFinder",
    "demosys.finders.program.EffectDirectoriesFinder",
)

PROGRAM_LOADERS = (
    'demosys.loaders.program.single.Loader',
    'demosys.loaders.program.separate.Loader',
)

TEXTURE_DIRS = (

)

TEXTURE_FINDERS = (
    "demosys.finders.textures.FileSystemFinder",
    "demosys.finders.textures.EffectDirectoriesFinder",
)

TEXTURE_LOADERS = (
    'demosys.loaders.texture.t2d.Loader',
    'demosys.loaders.texture.array.Loader',
)

SCENE_DIRS = (

)

SCENE_FINDERS = (
    "demosys.finders.scenes.FileSystemFinder",
    "demosys.finders.scenes.EffectDirectoriesFinder",
)

SCENE_LOADERS = (
    "demosys.loaders.scene.gltf.GLTF2",
    "demosys.loaders.scene.wavefront.ObjLoader",
    "demosys.loaders.scene.stl_loader.STLLoader",
)

DATA_DIRS = ()

DATA_FINDERS = (
    "demosys.finders.data.FileSystemFinder",
    "demosys.finders.data.EffectDirectoriesFinder",
)

DATA_LOADERS = (
    'demosys.loaders.data.binary.Loader',
    'demosys.loaders.data.text.Loader',
    'demosys.loaders.data.json.Loader',
)
