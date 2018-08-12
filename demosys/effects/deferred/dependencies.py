from demosys.resources.meta import ProgramDescription

effect_packages = []

resources = [
    ProgramDescription(label="demosys.deferred.point_light", path="deferred/light_point.glsl"),
    ProgramDescription(label="demosys.deferred.debug", path="deferred/debug.glsl"),
    ProgramDescription(label="demosys.deferred.combine", path="deferred/combine.glsl"),
]
