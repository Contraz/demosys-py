import numpy

from demosys.opengl import VAO
from demosys import context


def cube(width, height, depth, normals=True, uvs=True):
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

    pos = context.ctx().buffer(numpy.array([
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
    ], dtype=numpy.float32).tobytes())
    if normals:
        normals = context.ctx().buffer(numpy.array([
            -0, 0, 1,
            -0, 0, 1,
            -0, 0, 1,
            0, 0, 1,
            0, 0, 1,
            0, 0, 1,
            1, 0, 0,
            1, 0, 0,
            1, 0, 0,
            1, 0, 0,
            1, 0, 0,
            1, 0, 0,
            0, -1, 0,
            0, -1, 0,
            0, -1, 0,
            0, -1, 0,
            0, -1, 0,
            0, -1, 0,
            -1, -0, 0,
            -1, -0, 0,
            -1, -0, 0,
            -1, -0, 0,
            -1, -0, 0,
            -1, -0, 0,
            0, 0, -1,
            0, 0, -1,
            0, 0, -1,
            0, 0, -1,
            0, 0, -1,
            0, 0, -1,
            0, 1, 0,
            0, 1, 0,
            0, 1, 0,
            0, 1, 0,
            0, 1, 0,
            0, 1, 0,
        ], dtype=numpy.float32).tobytes())
    if uvs:
        uvs = context.ctx().buffer(numpy.array([
            1, 0,
            1, 1,
            0, 0,
            1, 1,
            0, 1,
            0, 0,
            1, 0,
            1, 1,
            0, 0,
            1, 1,
            0, 1,
            0, 0,
            1, 1,
            0, 1,
            0, 0,
            1, 1,
            0, 0,
            1, 0,
            0, 1,
            0, 0,
            1, 0,
            0, 1,
            1, 0,
            1, 1,
            1, 0,
            1, 1,
            0, 1,
            1, 0,
            0, 1,
            0, 0,
            1, 1,
            0, 1,
            1, 0,
            0, 1,
            0, 0,
            1, 0
        ], dtype=numpy.float32).tobytes())

    vao = VAO("geometry:cube")

    # Add buffers
    vao.buffer(pos, '3f', ['in_position'])
    if normals:
        vao.buffer(normals, '3f', ['in_normal'])
    if uvs:
        vao.buffer(uvs, '2f', ['in_uv'])

    return vao
