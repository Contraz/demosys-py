from pyrr import Matrix33


class MeshShader:

    def __init__(self, shader):
        self.shader = shader

    def draw(self, mesh, proj_mat, view_mat):
        """Minimal draw function. Should be overridden"""
        mesh.vao.bind(self.shader)
        self.shader.uniform_mat4("m_proj", proj_mat)
        self.shader.uniform_mat4("m_mv", view_mat)
        mesh.vao.draw()

    def apply(self, mesh):
        """
        Determine if this MeshShader should be applied to the mesh
        Can return self or some MeshShader instance to support dynamic MeshShader creation
        """
        raise NotImplementedError("apply is not implemented. Please override the MeshShader method")

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
