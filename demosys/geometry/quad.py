import numpy

import moderngl
from demosys.opengl.vao import VAO


def quad_fs() -> VAO:
    """
    Creates a screen aligned quad using two triangles with normals and texture coordiantes.

    Returns:
        A :py:class:`demosys.opengl.vao.VAO` instance.
    """
    return quad_2d(2.0, 2.0, 0.0, 0.0)


def quad_2d(width, height, xpos=0.0, ypos=0.0) -> VAO:
    """
    Creates a 2D quad VAO using 2 triangles with normals and texture coordinates.

    Args:
        width (float): Width of the quad
        height (float): Height of the quad

    Keyword Args:
        xpos (float): Center position x
        ypos (float): Center position y

    Returns:
        A :py:class:`demosys.opengl.vao.VAO` instance.
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
