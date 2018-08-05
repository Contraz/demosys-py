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

# Raise errors when shader uniforms are assigned incorrectly
# Otherwise just print the errors to terminal
SHADER_STRICT_VALIDATION = False

SHADERS = {
    'vertex_shader_suffix': ('vert', '_vs.glsl', '.glslv'),
    'fragment_shader_suffix': ('frag', '_fs.glsl', '.glslf'),
    'geometry_shader_suffix': ('geom', '_gs.glsl', '.glslg'),
}

SHADER_DIRS = ()

SHADER_FINDERS = (
    'demosys.core.shaderfiles.finders.FileSystemFinder',
    'demosys.core.shaderfiles.finders.EffectDirectoriesFinder'
)

TEXTURE_DIRS = ()

TEXTURE_FINDERS = (
    'demosys.core.texturefiles.finders.FileSystemFinder',
    'demosys.core.texturefiles.finders.EffectDirectoriesFinder'
)

TEXTURE_LOADERS = (
    'demosys.loaders.texture.Texture2D',
    'demosys.loaders.texture.TextureArray',
)

SCENE_DIRS = ()

SCENE_FINDERS = (
    "demosys.core.scenefiles.finders.FileSystemFinder",
    "demosys.core.scenefiles.finders.EffectDirectoriesFinder",
)

SCENE_LOADERS = (
    'demosys.loaders.scene.gltf.GLTF2',
    'demosys.loaders.scene.wavefront.ObjLoader',
)

DATA_DIRS = ()

DATA_FINDERS = (
    "demosys.core.datafiles.finders.FileSystemFinder",
    "demosys.core.datafiles.finders.EffectDirectoriesFinder",
)
