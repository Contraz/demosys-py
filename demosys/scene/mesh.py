"""
Mesh class containing geometry information
"""
from pyrr import Matrix33


class Mesh:
    def __init__(self, name, vao=None, material=None):
        self.name = name
        self.vao = vao
        self.material = material

    def draw(self, m_mv, m_proj, shader):
        m_normal = self.create_normal_matrix(m_mv)

        self.vao.bind(shader)
        if self.material and self.material.color:
            shader.uniform_4fv("color", self.material.color)
        else:
            shader.uniform_4fv("color", [1.0, 1.0, 1.0, 1.0])
        shader.uniform_mat4("m_proj", m_proj)
        shader.uniform_mat4("m_mv", m_mv)
        shader.uniform_mat3("m_normal", m_normal)
        self.vao.draw()

    def create_normal_matrix(self, modelview):
        """
        Convert to mat3 and return inverse transpose.
        These are normally needed when dealing with normals in shaders.

        :param modelview: The modelview matrix
        :return: Normal matrix
        """
        normal_m = Matrix33.from_matrix44(modelview)
        normal_m = normal_m.inverse
        normal_m = normal_m.transpose()
        return normal_m
