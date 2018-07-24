import numpy

import moderngl
from demosys.opengl import VAO


def bbox(width=1.0, height=1.0, depth=1.0):
    """
    Generates a bounding box.
    This is simply a box with LINE_STRIP as draw mode

    :param width: Width of the box
    :param height: height of the box
    :param depth: depth of the box
    :return: VAO
    """
    width, height, depth = width / 2.0, height / 2.0, depth / 2.0
    pos = numpy.array([
        width, -height, depth,
        width, height, depth,
        -width, -height, depth,
        width, height, depth,
        -width, height, depth,
        -width, -height, depth,
        width, -height, -depth,
        width, height, -depth,
        width, -height, depth,
        width, height, -depth,
        width, height, depth,
        width, -height, depth,
        width, -height, -depth,
        width, -height, depth,
        -width, -height, depth,
        width, -height, -depth,
        -width, -height, depth,
        -width, -height, -depth,
        -width, -height, depth,
        -width, height, depth,
        -width, height, -depth,
        -width, -height, depth,
        -width, height, -depth,
        -width, -height, -depth,
        width, height, -depth,
        width, -height, -depth,
        -width, -height, -depth,
        width, height, -depth,
        -width, -height, -depth,
        -width, height, -depth,
        width, height, -depth,
        -width, height, -depth,
        width, height, depth,
        -width, height, -depth,
        -width, height, depth,
        width, height, depth,
    ], dtype=numpy.float32)

    vao = VAO("geometry:cube", mode=moderngl.LINE_STRIP)
    vao.buffer(pos, '3f', ["in_position"])

    return vao
