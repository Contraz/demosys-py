import numpy

import moderngl
from demosys import context
from demosys.opengl import VAO


def quad_fs() -> VAO:
    """
    Creates a screen aligned quad.
    """
    return quad_2d(2.0, 2.0, 0.0, 0.0)


def quad_2d(width, height, xpos=0.0, ypos=0.0) -> VAO:
    """
    Creates a 2D quad VAO using 2 triangles.

    :param width: Width of the quad
    :param height: Height of the quad
    :param xpos: Center position x
    :param ypos: Center position y
    """
    pos = context.ctx().buffer(numpy.array([
        xpos - width / 2.0, ypos + height / 2.0, 0.0,
        xpos - width / 2.0, ypos - height / 2.0, 0.0,
        xpos + width / 2.0, ypos - height / 2.0, 0.0,
        xpos - width / 2.0, ypos + height / 2.0, 0.0,
        xpos + width / 2.0, ypos - height / 2.0, 0.0,
        xpos + width / 2.0, ypos + height / 2.0, 0.0,
    ], dtype=numpy.float32).tobytes())

    normals = context.ctx().buffer(numpy.array([
        0.0, 0.0, 1.0,
        0.0, 0.0, 1.0,
        0.0, 0.0, 1.0,
        0.0, 0.0, 1.0,
        0.0, 0.0, 1.0,
        0.0, 0.0, 1.0,
    ], dtype=numpy.float32).tobytes())

    uvs = context.ctx().buffer(numpy.array([
        0.0, 1.0,
        0.0, 0.0,
        1.0, 0.0,
        0.0, 1.0,
        1.0, 0.0,
        1.0, 1.0,
    ], dtype=numpy.float32).tobytes())

    vao = VAO("geometry:quad", mode=moderngl.TRIANGLES)
    vao.buffer(pos, '3f', ["in_position"])
    vao.buffer(normals, '3f', ["in_normal"])
    vao.buffer(uvs, '2f', ["in_uv"])

    return vao
