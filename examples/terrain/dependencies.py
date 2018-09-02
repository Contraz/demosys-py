from demosys.resources.meta import ProgramDescription, TextureDescription

effect_packages = []

resources = [
    # Program in one single file
    # ProgramDescription(label="terrain", path="terrain/terrain.glsl"),

    # Program split into separate shader files
    ProgramDescription(
        label="terrain",
        vertex_shader="terrain/terrain_vs.glsl",
        tess_control_shader="terrain/terrain_tc.glsl",
        tess_evaluation_shader="terrain/terrain_te.glsl",
        fragment_shader="terrain/terrain_fs.glsl",
    ),
    TextureDescription(label="heightmap", path="terrain/Ridges_01_DISP.jpg"),
]
