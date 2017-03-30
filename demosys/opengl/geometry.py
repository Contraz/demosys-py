from demosys.opengl import VAO
from OpenGL import GL
from OpenGL.arrays.vbo import VBO
import numpy


def quad_fs():
    return quad(2.0, 2.0, 0.0, 0.0)


def quad(width, height, xpos, ypos):
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
    vao = VAO("geometry:quad")
    vao.add_array_buffer(GL.GL_FLOAT, pos)
    vao.add_array_buffer(GL.GL_FLOAT, normals)
    vao.add_array_buffer(GL.GL_FLOAT, uvs)
    vao.map_buffer(pos, "in_Position", 3)
    vao.map_buffer(normals, "in_normal", 3)
    vao.map_buffer(uvs, "in_UV0", 2)
    vao.build()
    return vao


def plane(x, y, normals=True, uvs=True):
    return VAO()


def cube(size, normals=True, uvs=True):
    pos = VBO(numpy.array([
        size, -size, size,
        size, size, size,
        -size, -size, size,
        size, size, size,
        -size, size, size,
        -size, -size, size,
        size, -size, -size,
        size, size, -size,
        size, -size, size,
        size, size, -size,
        size, size, size,
        size, -size, size,
        size, -size, -size,
        size, -size, size,
        -size, -size, size,
        size, -size, -size,
        -size, -size, size,
        -size, -size, -size,
        -size, -size, size,
        -size, size, size,
        -size, size, -size,
        -size, -size, size,
        -size, size, -size,
        -size, -size, -size,
        size, size, -size,
        size, -size, -size,
        -size, -size, -size,
        size, size, -size,
        -size, -size, -size,
        -size, size, -size,
        size, size, -size,
        -size, size, -size,
        size, size, size,
        -size, size, -size,
        -size, size, size,
        size, size, size,
    ], dtype=numpy.float32))
    normals = VBO(numpy.array([
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
    ], dtype=numpy.float32))
    uvs = VBO(numpy.array([
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
    ], dtype=numpy.float32))

    vao = VAO("geometry:cube")
    vao.add_array_buffer(GL.GL_FLOAT, pos)
    vao.add_array_buffer(GL.GL_FLOAT, normals)
    vao.add_array_buffer(GL.GL_FLOAT, uvs)
    vao.map_buffer(pos, "in_Position", 3)
    vao.map_buffer(normals, "in_Normal", 3)
    vao.map_buffer(uvs, "in_UV0", 2)
    vao.build()
    return vao
