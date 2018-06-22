import math
import moderngl as mlg
import numpy

from demosys import context
from demosys.opengl import VAO


def sphere(radius=0.5, sectors=32, rings=16):
    """
    Generate a sphere

    :param radius: Radius or the sphere
    :param rings: number or horizontal rings
    :param sectors: number of vertical segments
    :return: VAO containing the sphere
    """
    R = 1.0 / (rings - 1)
    S = 1.0 / (sectors - 1)

    vertices = [0] * (rings * sectors * 3)
    normals = [0] * (rings * sectors * 3)
    uvs = [0] * (rings * sectors * 2)

    v, n, t = 0, 0, 0
    for r in range(rings):
        for s in range(sectors):
            y = math.sin(-math.pi / 2 + math.pi * r * R)
            x = math.cos(2 * math.pi * s * S) * math.sin(math.pi * r * R)
            z = math.sin(2 * math.pi * s * S) * math.sin(math.pi * r * R)

            uvs[t] = s * S
            uvs[t + 1] = r * R

            vertices[v] = x * radius
            vertices[v + 1] = y * radius
            vertices[v + 2] = z * radius

            normals[n] = x
            normals[n + 1] = y
            normals[n + 2] = z

            t += 2
            v += 3
            n += 3

    indices = [0] * rings * sectors * 6
    i = 0
    for r in range(rings - 1):
        for s in range(sectors - 1):
            indices[i] = r * sectors + s
            indices[i + 1] = (r + 1) * sectors + (s + 1)
            indices[i + 2] = r * sectors + (s + 1)

            indices[i + 3] = r * sectors + s
            indices[i + 4] = (r + 1) * sectors + s
            indices[i + 5] = (r + 1) * sectors + (s + 1)
            i += 6

    vbo_vertices = context.ctx().buffer(numpy.array(vertices, dtype=numpy.float32).tobytes())
    vbo_normals = context.ctx().buffer(numpy.array(normals, dtype=numpy.float32).tobytes())
    vbo_uvs = context.ctx().buffer(numpy.array(uvs, dtype=numpy.float32).tobytes())
    vbo_elements = context.ctx().buffer(numpy.array(indices, dtype=numpy.uint32).tobytes())

    vao = VAO("sphere", mode=mlg.TRIANGLES)
    # VBOs
    vao.buffer(vbo_vertices, '3f', ['in_position'])
    vao.buffer(vbo_normals, '3f', ['in_normal'])
    vao.buffer(vbo_uvs, '2f', ['in_uv'])
    vao.index_buffer('u', vbo_elements)

    return vao
