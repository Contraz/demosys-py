import random

import numpy

import moderngl
from demosys.opengl.vao import VAO


def points_random_3d(count, range_x=(-10.0, 10.0), range_y=(-10.0, 10.0), range_z=(-10.0, 10.0), seed=None) -> VAO:
    """
    Generates random positions inside a confied box.

    Args:
        count (int): Number of points to generate

    Keyword Args:
        range_x (tuple): min-max range for x axis: Example (-10.0. 10.0)
        range_y (tuple): min-max range for y axis: Example (-10.0. 10.0)
        range_z (tuple): min-max range for z axis: Example (-10.0. 10.0)
        seed (int): The random seed

    Returns:
        A :py:class:`demosys.opengl.vao.VAO` instance
    """
    random.seed(seed)

    def gen():
        for _ in range(count):
            yield random.uniform(*range_x)
            yield random.uniform(*range_y)
            yield random.uniform(*range_z)

    data = numpy.fromiter(gen(), count=count * 3, dtype=numpy.float32)

    vao = VAO("geometry:points_random_3d", mode=moderngl.POINTS)
    vao.buffer(data, '3f', ['in_position'])

    return vao
