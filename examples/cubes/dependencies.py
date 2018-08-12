from demosys.resources.meta import TextureDescription, ProgramDescription

effect_packages = []

resources = [
    ProgramDescription(label="plain", path="cubes/cube_plain.glsl"),
    ProgramDescription(label="light", path="cubes/cube_light.glsl"),
    ProgramDescription(
        label="textured", 
        vertex_shader="cubes/cube_textured_vs.glsl",
        fragment_shader="cubes/cube_textured_fs.glsl",
    ),
    TextureDescription( label="crate", path="cubes/crate.jpg"),
]
