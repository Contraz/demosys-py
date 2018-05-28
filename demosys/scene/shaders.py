import os
from pyrr import Matrix33
from demosys.conf import settings
from demosys.resources import shaders

settings.add_shader_dir(os.path.join(os.path.dirname(__file__), 'shaders'))


class MeshShader:

    def __init__(self, shader=None, **kwargs):
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


class ColorShader(MeshShader):
    """
    Simple color shader
    """
    def __init__(self, shader=None, **kwargs):
        super().__init__(shader=shaders.get("scene_default/color.glsl", create=True))

    def draw(self, mesh, proj_mat, view_mat):
        m_normal = self.create_normal_matrix(view_mat)

        mesh.vao.bind(self.shader)

        if mesh.material and mesh.material.color:
            self.shader.uniform_4fv("color", mesh.material.color)
        else:
            self.shader.uniform_4fv("color", [1.0, 1.0, 1.0, 1.0])

        self.shader.uniform_mat4("m_proj", proj_mat)
        self.shader.uniform_mat4("m_mv", view_mat)
        self.shader.uniform_mat3("m_normal", m_normal)

        mesh.vao.draw()

    def apply(self, mesh):
        if not mesh.material:
            return None

        if mesh.material.mat_texture is None:
            return self
        return None


class TextureShader(MeshShader):
    """
    Simple texture shader
    """
    def __init__(self, shader=None, **kwargs):
        super().__init__(shader=shaders.get("scene_default/texture.glsl", create=True))

    def draw(self, mesh, proj_mat, view_mat):
        m_normal = self.create_normal_matrix(view_mat)

        mesh.vao.bind(self.shader)
        self.shader.uniform_sampler_2d(0, "texture0", mesh.material.mat_texture.texture,
                                       sampler=mesh.material.mat_texture.sampler)
        self.shader.uniform_mat4("m_proj", proj_mat)
        self.shader.uniform_mat4("m_mv", view_mat)
        self.shader.uniform_mat3("m_normal", m_normal)

        mesh.vao.draw()

    def apply(self, mesh):
        if not mesh.material:
            return None

        if mesh.material.mat_texture is not None:
            return self

        return None


class FallbackShader(MeshShader):
    """
    Fallback shader only rendering positions in white
    """
    def __init__(self, shader=None, **kwargs):
        super().__init__(shader=shaders.get("scene_default/fallback.glsl", create=True))

    def draw(self, mesh, proj_mat, view_mat):
        mesh.vao.bind(self.shader)
        self.shader.uniform_mat4("m_proj", proj_mat)
        self.shader.uniform_mat4("m_mv", view_mat)
        mesh.vao.draw()

    def apply(self, mesh):
        return self
