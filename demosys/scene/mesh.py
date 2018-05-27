"""
Mesh class containing geometry information
"""
from pyrr import Matrix33


class Mesh:
    def __init__(self, name, vao=None, material=None, attributes=None):
        """
        :param name: Name of the mesh
        :param vao: VAO
        :param material: Material
        :param attributes: Details info about each mesh attribute (dict)
            {
                "NORMAL": {"name": "in_normal", "components": 3, "type": GL_FLOAT},
                "POSITION": {"name": "in_position", "components": 3, "type": GL_FLOAT}
            }
        """
        self.name = name
        self.vao = vao
        self.material = material
        self.attributes = attributes
        self.shader = None

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

    def has_normals(self):
        return "NORMAL" in self.attributes

    def has_uvs(self, layer=0):
        return "TEXCOORD_{}".format(layer) in self.attributes

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
