from demosys.resources.meta import ProgramDescription, TextureDescription

effect_packages = []

resources = [
    ProgramDescription(label="cube_multi_fade", path='geocubes/cube_multi_fade.glsl'),
    ProgramDescription(label="cube_texture_light", path='geocubes/cube_texture_light.glsl'),
    ProgramDescription(label="quad_fs_uvscale", path='geocubes/quad_fs_uvscale.glsl'),

    TextureDescription(label="texture", path='geocubes/texture.png'),
    TextureDescription(label="GreenFabric", path='geocubes/GreenFabric.png'),
]
