from demosys.resources import TextureDescription, ProgramDescription


resources = [
    TextureDescription(path="cubes/crate.jpg", label="crate"),

    ProgramDescription(path="cubes/cube_plain.glsl", label="plain"),
    ProgramDescription(path="cubes/cube_light.glsl", label="light"),
    ProgramDescription(path="cubes/cube_textured.glsl", label="textured"),
]
