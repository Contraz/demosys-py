import numpy

import moderngl
from demosys.opengl import VAO

# Cache fullscreen quad
QUAD_FS = None


def quad_fs() -> VAO:
    """
    Creates a screen aligned quad.
    """
    global QUAD_FS
    if not QUAD_FS:
        QUAD_FS = quad_2d(2.0, 2.0, 0.0, 0.0)
    return QUAD_FS


def quad_2d(width, height, xpos=0.0, ypos=0.0) -> VAO:
    """
    Creates a 2D quad VAO using 2 triangles.

    :param width: Width of the quad
    :param height: Height of the quad
    :param xpos: Center position x
    :param ypos: Center position y
    """
    pos = numpy.array([
        xpos - width / 2.0, ypos + height / 2.0, 0.0,
        xpos - width / 2.0, ypos - height / 2.0, 0.0,
        xpos + width / 2.0, ypos - height / 2.0, 0.0,
        xpos - width / 2.0, ypos + height / 2.0, 0.0,
        xpos + width / 2.0, ypos - height / 2.0, 0.0,
        xpos + width / 2.0, ypos + height / 2.0, 0.0,
    ], dtype=numpy.float32)

    normals = numpy.array([
        0.0, 0.0, 1.0,
        0.0, 0.0, 1.0,
        0.0, 0.0, 1.0,
        0.0, 0.0, 1.0,
        0.0, 0.0, 1.0,
        0.0, 0.0, 1.0,
    ], dtype=numpy.float32)

    uvs = numpy.array([
        0.0, 1.0,
        0.0, 0.0,
        1.0, 0.0,
        0.0, 1.0,
        1.0, 0.0,
        1.0, 1.0,
    ], dtype=numpy.float32)

    vao = VAO("geometry:quad", mode=moderngl.TRIANGLES)
    vao.buffer(pos, '3f', ["in_position"])
    vao.buffer(normals, '3f', ["in_normal"])
    vao.buffer(uvs, '2f', ["in_uv"])

    return vao
