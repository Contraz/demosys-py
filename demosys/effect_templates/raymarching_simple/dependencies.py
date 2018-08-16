import os

from demosys.resources.meta import ProgramDescription


def local(path):
    """
    Prepend the effect package name to a path so resources
    can still be loaded when copied into a new effect package.
    """
    return os.path.join(__name__.split('.')[-2], path)


effect_packages = []

resources = [
    ProgramDescription(label="raymarching_simple", path=local("raymarching_simple.glsl")),
]
