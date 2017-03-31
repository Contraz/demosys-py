import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

DEBUG = False

# Profile: any, core, compat
OPENGL = {
    "version": (4, 1),
    "profile": "core",
    "forward_compat": True,
}

WINDOW = {
    # "size": (640, 360),
    "size": (1280, 768),
    # "size": (1000, 600),
    "vsync": True,
    "resizable": False,
    "fullscreen": False,
    "title": "demosys-py",
}

MUSIC = os.path.join(PROJECT_DIR, 'resources/music/tg2035.mp3')

# What effects to load
EFFECTS = (
    'demosys_test.cube',
)

SHADER_DIRS = (
    os.path.join(PROJECT_DIR, 'resources/shaders'),
)

SHADER_FINDERS = (
    'demosys.core.shaderfiles.finders.FileSystemFinder',
    'demosys.core.shaderfiles.finders.EffectDirectoriesFinder',
)

# Hardcoded paths to shader dirs
TEXTURE_DIRS = (
    os.path.join(PROJECT_DIR, 'resource/textures'),
)

# Finder classes
TEXTURE_FINDERS = (
    'demosys.core.texturefiles.finders.FileSystemFinder',
    'demosys.core.texturefiles.finders.EffectDirectoriesFinder'
)

# Tell demosys how to find shaders split into multiple files
SHADERS = {
    'vertex_shader_suffix': ('vert', '_vs.glsl', '.glslv'),
    'fragment_shader_suffix': ('frag', '_fs.glsl', '.glslf'),
    'geometry_shader_suffix': ('geom', '_gs.glsl', '.glslg'),
}
