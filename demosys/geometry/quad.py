import moderngl as mgl
import numpy
from demosys.opengl import VAO
from demosys import context

# Cache fullscreen quad
QUAD_FS = None


def quad_fs():
    """
    Creates a screen aligned quad.
    """
    global QUAD_FS
    if not QUAD_FS:
        QUAD_FS = quad_2d(2.0, 2.0, 0.0, 0.0)
    return QUAD_FS


def quad_2d(width, height, xpos=0.0, ypos=0.0):
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

    vao = VAO("geometry:quad", mode=mgl.TRIANGLES)
    vao.buffer(pos, '3f', ["in_position"])
    vao.buffer(normals, '3f', ["in_normal"])
    vao.buffer(uvs, '2f', ["in_uv"])

    return vao
