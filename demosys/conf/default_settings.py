"""
Default settings for demosys. Override using a settings module.
"""

# What attributes should be used when generating a settings file
__ORDER__ = (
    'DEBUG',
    'SCREENSHOT_PATH',
    'OPENGL',
    'WINDOW',
    'MUSIC',
    'TIMER',
    'ROCKET',
    'EFFECTS',
    'EFFECT_MANAGER',
    'SHADER_DIRS',
    'SHADER_FINDERS',
    'TEXTURE_DIRS',
    'TEXTURE_FINDERS',
    'SCENE_DIRS',
    'SCENE_FINDERS',
    'SCENE_LOADERS',
    'DATA_DIRS',
    'DATA_FINDERS',
)

DEBUG = False

SCREENSHOT_PATH = None

# OpenGL context configuration
# version: (MAJOR, MINOR)
OPENGL = {
    "version": (3, 3),
}

# Window size
WINDOW = {
    "class": "demosys.context.glfw.GLFW_Window",
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

TIMER = 'demosys.timers.Timer'

ROCKET = {
    'mode': 'editor',
    'rps': 24,
    'project': None,
    'files': None,
}

# Empty effects tuple
EFFECTS = ()

EFFECT_MANAGER = 'demosys.effects.managers.SingleEffectManager'

# Raise errors when uniforms are assigned with incorrect type
# Otherwise just print the errors to terminal
SHADER_STRICT_VALIDATION = False

SHADERS = {
    'vertex_shader_suffix': ('vert', '_vs.glsl', '.glslv'),
    'fragment_shader_suffix': ('frag', '_fs.glsl', '.glslf'),
    'geometry_shader_suffix': ('geom', '_gs.glsl', '.glslg'),
}

# Additional directories shaders can be found
SHADER_DIRS = ()

# Finder
SHADER_FINDERS = (
    'demosys.core.shaderfiles.finders.FileSystemFinder',
    'demosys.core.shaderfiles.finders.EffectDirectoriesFinder'
)

# Additonal directories textures can be found
TEXTURE_DIRS = ()
TEXTURE_FINDERS = (
    'demosys.core.texturefiles.finders.FileSystemFinder',
    'demosys.core.texturefiles.finders.EffectDirectoriesFinder'
)

SCENE_DIRS = ()
SCENE_FINDERS = (
    "demosys.core.scenefiles.finders.FileSystemFinder",
    "demosys.core.scenefiles.finders.EffectDirectoriesFinder",
)

SCENE_LOADERS = (
    'demosys.scene.loaders.gltf.GLTF2',
    'demosys.scene.loaders.wavefront.ObjLoader',
)

DATA_DIRS = ()
DATA_FINDERS = (
    "demosys.core.datafiles.finders.FileSystemFinder",
    "demosys.core.datafiles.finders.EffectDirectoriesFinder",
)
