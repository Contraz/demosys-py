from demosys.resources.meta import ProgramDescription, TextureDescription

effect_packages = []

resources = [
    ProgramDescription(label="transform", path="feedback/transform.glsl"),
    ProgramDescription(label="billboards", path="feedback/billboards.glsl"),
    TextureDescription(label="particle", path="feedback/particle.png"),
]
