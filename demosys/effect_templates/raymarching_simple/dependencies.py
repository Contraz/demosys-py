import os

from demosys.resources.meta import ProgramDescription


def local(path):
    """Get the effect package name"""
    return os.path.join(__name__.split('.')[-2], path)


effect_packages = []

resources = [
    ProgramDescription(label="raymarching_simple", path=local("raymarching_simple.glsl")),
]
