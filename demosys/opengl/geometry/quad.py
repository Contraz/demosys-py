from demosys.opengl import VAO
from OpenGL import GL
from OpenGL.arrays.vbo import VBO
import numpy


def quad_fs():
    """
    Creates a screen aligned quad.
    """
    return quad_2d(2.0, 2.0, 0.0, 0.0)


def quad_2d(width, height, xpos=0.0, ypos=0.0):
    """
    Creates a 2D quad VAO using 2 triangles.

    :param width: Width of the quad
    :param height: Height of the quad
    :param xpos: Center position x
    :param ypos: Center position y
    """
    pos = VBO(numpy.array([
        xpos - width / 2.0, ypos + height / 2.0, 0.0,
        xpos - width / 2.0, ypos - height / 2.0, 0.0,
        xpos + width / 2.0, ypos - height / 2.0, 0.0,
        xpos - width / 2.0, ypos + height / 2.0, 0.0,
        xpos + width / 2.0, ypos - height / 2.0, 0.0,
        xpos + width / 2.0, ypos + height / 2.0, 0.0,
    ], dtype=numpy.float32))
    normals = VBO(numpy.array([
        0.0, 0.0, 1.0,
        0.0, 0.0, 1.0,
        0.0, 0.0, 1.0,
        0.0, 0.0, 1.0,
        0.0, 0.0, 1.0,
        0.0, 0.0, 1.0,
    ], dtype=numpy.float32))
    uvs = VBO(numpy.array([
        0.0, 1.0,
        0.0, 0.0,
        1.0, 0.0,
        0.0, 1.0,
        1.0, 0.0,
        1.0, 1.0,
    ], dtype=numpy.float32))
    vao = VAO("geometry:quad", mode=GL.GL_TRIANGLES)
    vao.add_array_buffer(GL.GL_FLOAT, pos)
    vao.add_array_buffer(GL.GL_FLOAT, normals)
    vao.add_array_buffer(GL.GL_FLOAT, uvs)
    vao.map_buffer(pos, "in_position", 3)
    vao.map_buffer(normals, "in_normal", 3)
    vao.map_buffer(uvs, "in_uv", 2)
    vao.build()
    return vao
