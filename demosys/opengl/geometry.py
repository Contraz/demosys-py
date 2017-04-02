from demosys.opengl import VAO
from OpenGL import GL
from OpenGL.arrays.vbo import VBO
import numpy
import random


def quad_fs():
    return quad_2d(2.0, 2.0, 0.0, 0.0)


def quad_2d(width, height, xpos, ypos):
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
    vao.map_buffer(pos, "in_position", 3)
    vao.map_buffer(normals, "in_normal", 3)
    vao.map_buffer(uvs, "in_uv", 2)
    vao.build()
    return vao


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
    width, height, depth = width / 2, height / 2, depth / 2
    pos = VBO(numpy.array([
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
    ], dtype=numpy.float32))
    if normals:
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
    if uvs:
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
    if normals:
        vao.add_array_buffer(GL.GL_FLOAT, normals)
    if uvs:
        vao.add_array_buffer(GL.GL_FLOAT, uvs)
    vao.map_buffer(pos, "in_position", 3)
    if normals:
        vao.map_buffer(normals, "in_normal", 3)
    if uvs:
        vao.map_buffer(uvs, "in_uv", 2)
    vao.build()
    return vao


def points_random_3d(count, range_x=(-10.0, 10.0), range_y=(-10.0, 10.0), range_z=(-10.0, 10.0), seed=None):
    """
    Generates random positions
    :param count: Number of points
    :param range_x: min-max range for x axis
    :param range_y: min-max range for y axis
    :param range_z: min-max range for z axis
    """
    random.seed(seed)

    def gen():
        for i in range(count):
            # yield random.random() * (range_x[1] - range_x[0]) - range_x[0]
            # yield random.random() * (range_y[1] - range_y[0]) - range_y[0]
            # yield random.random() * (range_z[1] - range_z[0]) - range_z[0]
            yield random.uniform(*range_x)
            yield random.uniform(*range_y)
            yield random.uniform(*range_z)

    pos = VBO(numpy.array(list(gen()), dtype=numpy.float32))
    vao = VAO("geometry:points_random_3d")
    vao.add_array_buffer(GL.GL_FLOAT, pos)
    vao.map_buffer(pos, "in_position", 3)
    vao.build()
    return vao
