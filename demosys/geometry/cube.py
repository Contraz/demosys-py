import numpy

from demosys.opengl import VAO


def cube(width, height, depth, center=(0.0, 0.0, 0.0), normals=True, uvs=True) -> VAO:
    """
    Generates a cube VAO. The cube center is (0.0, 0.0 0.0) unless other is specified.

    :param width: Width of the cube
    :param height: height of the cube
    :param depth: depth of the cube
    :param center: center of the cube
    :param normals: (bool) Include normals
    :param uvs: (bool) include uv coordinates
    :return: VAO representing the cube
    """
    width, height, depth = width / 2.0, height / 2.0, depth / 2.0

    pos = numpy.array([
        center[0] + width, center[1] - height, center[2] + depth,
        center[0] + width, center[1] + height, center[2] + depth,
        center[0] - width, center[1] - height, center[2] + depth,
        center[0] + width, center[1] + height, center[2] + depth,
        center[0] - width, center[1] + height, center[2] + depth,
        center[0] - width, center[1] - height, center[2] + depth,
        center[0] + width, center[1] - height, center[2] - depth,
        center[0] + width, center[1] + height, center[2] - depth,
        center[0] + width, center[1] - height, center[2] + depth,
        center[0] + width, center[1] + height, center[2] - depth,
        center[0] + width, center[1] + height, center[2] + depth,
        center[0] + width, center[1] - height, center[2] + depth,
        center[0] + width, center[1] - height, center[2] - depth,
        center[0] + width, center[1] - height, center[2] + depth,
        center[0] - width, center[1] - height, center[2] + depth,
        center[0] + width, center[1] - height, center[2] - depth,
        center[0] - width, center[1] - height, center[2] + depth,
        center[0] - width, center[1] - height, center[2] - depth,
        center[0] - width, center[1] - height, center[2] + depth,
        center[0] - width, center[1] + height, center[2] + depth,
        center[0] - width, center[1] + height, center[2] - depth,
        center[0] - width, center[1] - height, center[2] + depth,
        center[0] - width, center[1] + height, center[2] - depth,
        center[0] - width, center[1] - height, center[2] - depth,
        center[0] + width, center[1] + height, center[2] - depth,
        center[0] + width, center[1] - height, center[2] - depth,
        center[0] - width, center[1] - height, center[2] - depth,
        center[0] + width, center[1] + height, center[2] - depth,
        center[0] - width, center[1] - height, center[2] - depth,
        center[0] - width, center[1] + height, center[2] - depth,
        center[0] + width, center[1] + height, center[2] - depth,
        center[0] - width, center[1] + height, center[2] - depth,
        center[0] + width, center[1] + height, center[2] + depth,
        center[0] - width, center[1] + height, center[2] - depth,
        center[0] - width, center[1] + height, center[2] + depth,
        center[0] + width, center[1] + height, center[2] + depth,
    ], dtype=numpy.float32)

    if normals:
        normal_data = numpy.array([
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
        ], dtype=numpy.float32)

    if uvs:
        uvs_data = numpy.array([
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
        ], dtype=numpy.float32)

    vao = VAO("geometry:cube")

    # Add buffers
    vao.buffer(pos, '3f', ['in_position'])
    if normals:
        vao.buffer(normal_data, '3f', ['in_normal'])
    if uvs:
        vao.buffer(uvs_data, '2f', ['in_uv'])

    return vao
