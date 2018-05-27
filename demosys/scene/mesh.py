"""
Mesh class containing geometry information
"""


class Mesh:
    """Mesh info and geometry"""

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
        self.mesh_shader = None

    def draw(self, view_mat, proj_mat):
        """Draw the mesh using the assigned mesh shader"""
        if self.mesh_shader:
            self.mesh_shader.draw(self, proj_mat, view_mat)

    def has_normals(self):
        return "NORMAL" in self.attributes

    def has_uvs(self, layer=0):
        return "TEXCOORD_{}".format(layer) in self.attributes
