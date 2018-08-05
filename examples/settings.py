# Auto generated settings file
import os
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

SCREENSHOT_PATH = None

OPENGL = {
    "version": (3, 3),
}

WINDOW = {
    "class": "demosys.context.glfw.GLFW_Window",
    "size": (1280, 720),
    "aspect_ratio": 1.7777777777777777,
    "fullscreen": False,
    "resizable": True,
    "title": "Examples",
    "vsync": False,
    "cursor": True,
    "samples": 4,
}

HEADLESS_DURATION = 10.0

MUSIC = None

ROCKET = {
    "mode": "editor",
    "rps": 24,
    "project": None,
    "files": None,
}

EFFECTS = (

)

SHADER_DIRS = (

)

SHADER_FINDERS = (
    "demosys.core.shaderfiles.finders.FileSystemFinder",
    "demosys.core.shaderfiles.finders.EffectDirectoriesFinder",
)

TEXTURE_DIRS = (

)

TEXTURE_FINDERS = (
    "demosys.core.texturefiles.finders.FileSystemFinder",
    "demosys.core.texturefiles.finders.EffectDirectoriesFinder",
)

SCENE_DIRS = (

)

SCENE_FINDERS = (
    "demosys.core.scenefiles.finders.FileSystemFinder",
    "demosys.core.scenefiles.finders.EffectDirectoriesFinder",
)

SCENE_LOADERS = (
    "demosys.loaders.scene.gltf.GLTF2",
    "demosys.loaders.scene.wavefront.ObjLoader",
)
