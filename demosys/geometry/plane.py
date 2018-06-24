import moderngl as mgl
import numpy
from demosys.opengl import VAO


def plane_xz(size=(10, 10), resolution=(10, 10)):
    """
    Generates a plane on the xz axis of a specific size and resolution

    :param size: (x, y) tuple
    :param resolution: (x, y) tuple
    :return: VAO
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
        for z in range(rx * rz):
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

    vao = VAO("plane_xz", mode=mgl.TRIANGLES)

    vao.buffer(pos_data, '3f', ['in_position'])
    vao.buffer(uv_data, '2f', ['in_uv'])
    vao.buffer(normal_data, '3f', ['in_normal'])

    vao.index_buffer('u1', index_data)

    return vao


# def plane_xz(size=(10, 10), resolution=(10, 10)):
#     """
#     Generates a plane on the xz axis of a specific size and resolution
#     :param size: (x, y) tuple
#     :param resolution: (x, y) tuple
#     :return: VAO
#     """
#     sx, sz = size
#     rx, rz = resolution
#     dx, dz = sx / rx, sz / rz  # step
#     ox, oz = -sx / 2, -sz / 2  # start offset
#
#     def vertex(x, z):
#         yield ox + x * dx
#         yield 0
#         yield oz + z * dz
#
#     def uv(x, z):
#         yield x * 1 / rx
#         yield z * 1 / rz
#
#     def gen_pos():
#         up = True
#         for x in range(rx):
#             if up:
#                 # Generate strip upwards
#                 for z in reversed(range(rz)):
#                     yield from vertex(x, z)
#                     yield from vertex(x + 1, z)
#             else:
#                 # Generate strip downwards
#                 for z in range(rz - 1):
#                     yield from vertex(x + 1, z)
#                     yield from vertex(x, z + 1)
#
#             up = not up  # toggle strip direction
#
#     def gen_uv():
#         up = True
#         for x in range(rx):
#             if up:
#                 # Generate strip upwards
#                 for z in range(rz):
#                     yield from uv(x, z)
#                     yield from uv(x + 1, z)
#             else:
#                 # Generate strip downwards
#                 for z in range(rz - 1):
#                     yield from uv(x + 1, z)
#                     yield from uv(x, z + 1)
#
#     pos_data = numpy.fromiter(gen_pos(), dtype=numpy.float32)
#     position_vbo = VBO(pos_data)
#
#     uv_data = numpy.fromiter(gen_uv(), dtype=numpy.float32)
#     uv_vbo = VBO(uv_data)
#
#     vao = VAO("plane_xz", mode=GL.GL_TRIANGLE_STRIP)
#     vao.add_array_buffer(GL.GL_FLOAT, position_vbo)
#     vao.add_array_buffer(GL.GL_FLOAT, uv_vbo)
#     vao.map_buffer(position_vbo, "in_position", 3)
#     vao.map_buffer(uv_vbo, "in_uv", 2)
#     vao.build()
#     return vao
