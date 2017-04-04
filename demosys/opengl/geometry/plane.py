import numpy
from demosys.opengl import VAO
from OpenGL import GL
from OpenGL.arrays.vbo import VBO


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

    def vertex(x, z):
        yield ox + x * dx
        yield 0
        yield oz + z * dz

    def gen():
        up = True
        for x in range(rx):
            if up:
                # Generate strip upwards
                for z in reversed(range(rz)):
                    yield from vertex(x, z)
                    yield from vertex(x + 1, z)
            else:
                # Generate strip downwards
                for z in range(rz - 1):
                    yield from vertex(x + 1, z)
                    yield from vertex(x, z + 1)

            up = not up  # toggle strip direction

    # FIXME: Calculate the actual size (count=rx * rz * 3 * 2)
    data = numpy.fromiter(gen(), dtype=numpy.float32)
    position_vbo = VBO(data)

    vao = VAO("plane_xz", mode=GL.GL_TRIANGLE_STRIP)
    vao.add_array_buffer(GL.GL_FLOAT, position_vbo)
    vao.map_buffer(position_vbo, "in_position", 3)
    vao.build()
    return vao
