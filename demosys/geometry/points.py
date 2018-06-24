import moderngl as mgl
from demosys.opengl import VAO
import numpy
import random


def points_random_3d(count, range_x=(-10.0, 10.0), range_y=(-10.0, 10.0), range_z=(-10.0, 10.0), seed=None):
    """
    Generates random positions

    :param count: Number of points
    :param range_x: min-max range for x axis
    :param range_y: min-max range for y axis
    :param range_z: min-max range for z axis
    :param seed: The random seed to be used
    """
    random.seed(seed)

    def gen():
        for i in range(count):
            yield random.uniform(*range_x)
            yield random.uniform(*range_y)
            yield random.uniform(*range_z)

    data = numpy.fromiter(gen(), count=count * 3, dtype=numpy.float32)

    vao = VAO("geometry:points_random_3d", mode=mgl.POINTS)
    vao.buffer(data, '3f', ['in_position'])

    return vao
