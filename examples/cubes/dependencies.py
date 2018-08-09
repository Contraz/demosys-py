from demosys.resources.meta import TextureDescription, ProgramDescription

effect_packages = []

resources = [
    ProgramDescription(path="cubes/cube_plain.glsl", label="plain"),
    ProgramDescription(path="cubes/cube_light.glsl", label="light"),
    ProgramDescription(path="cubes/cube_textured.glsl", label="textured"),
    TextureDescription(path="cubes/crate.jpg", label="crate"),
]
