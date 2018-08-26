import numpy

import moderngl
from demosys.opengl.vao import VAO


def plane_xz(size=(10, 10), resolution=(10, 10)) -> VAO:
    """
    Generates a plane on the xz axis of a specific size and resolution.
    Normals and texture coordinates are also included.

    Args:
        size: (x, y) tuple
        resolution: (x, y) tuple

    Returns:
        A :py:class:`demosys.opengl.vao.VAO` instance
    """
    sx, sz = size
    rx, rz = resolution
    dx, dz = sx / rx, sz / rz  # step
    ox, oz = -sx / 2, -sz / 2  # start offset

    def gen_pos():
        for z in range(rz):
            for x in range(rx):
                yield ox + x * dx
                yield 0
                yield oz + z * dz

    def gen_uv():
        for z in range(rz):
            for x in range(rx):
                yield x / (rx - 1)
                yield 1 - z / (rz - 1)

    def gen_normal():
        for _ in range(rx * rz):
            yield 0.0
            yield 1.0
            yield 0.0

    def gen_index():
        for z in range(rz - 1):
            for x in range(rx - 1):
                # quad poly left
                yield z * rz + x + 1
                yield z * rz + x
                yield z * rz + x + rx
                # quad poly right
                yield z * rz + x + 1
                yield z * rz + x + rx
                yield z * rz + x + rx + 1

    pos_data = numpy.fromiter(gen_pos(), dtype=numpy.float32)
    uv_data = numpy.fromiter(gen_uv(), dtype=numpy.float32)
    normal_data = numpy.fromiter(gen_normal(), dtype=numpy.float32)
    index_data = numpy.fromiter(gen_index(), dtype=numpy.uint32)

    vao = VAO("plane_xz", mode=moderngl.TRIANGLES)

    vao.buffer(pos_data, '3f', ['in_position'])
    vao.buffer(uv_data, '2f', ['in_uv'])
    vao.buffer(normal_data, '3f', ['in_normal'])

    vao.index_buffer(index_data, index_element_size=4)

    return vao
