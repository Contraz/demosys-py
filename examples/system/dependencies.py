import os

from demosys.resources.meta import ProgramDescription, TextureDescription


def local(path):
    """
    Prepend the effect package name to a path so resources
    can still be loaded when copied into a new effect package.
    """
    return os.path.join(__name__.split('.')[-2], path)


effect_packages = []

resources = [
    TextureDescription(label='milkyway', path=local('MilkyWayPanorama4K.jpg')),
    ProgramDescription(label='milkyway', path=local('milkyway.glsl')),

    TextureDescription(label='sun', path=local('2k_sun.jpg'), mipmap=True),
    ProgramDescription(label='sun', path=local('sun.glsl')),

    TextureDescription(label='earth_day', path=local('2k_earth_daymap.jpg'), mipmap=True),
    TextureDescription(label='earth_night', path=local('2k_earth_nightmap.jpg'), mipmap=True),
    TextureDescription(label='earth_clouds', path=local('2k_earth_clouds.jpg'), mipmap=True),
    ProgramDescription(label='earth', path=local('earth.glsl')),
]
