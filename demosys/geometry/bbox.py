import moderngl as mgl
import numpy

from demosys.opengl import VAO


def bbox(width=1.0, height=1.0, depth=1.0):
    """
    Generates a cube centered at 0, 0, 0

    :param width: Width of the cube
    :param height: height of the cube
    :param depth: depth of the bubs
    :param normals: (bool) Include normals
    :param uvs: (bool) include uv coordinates
    :return: VAO representing the cube
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

    vao = VAO("geometry:cube", mode=mgl.LINE_STRIP)
    vao.buffer(pos, '3f', ["in_position"])

    return vao
