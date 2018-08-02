import os

from demosys import context
from demosys.conf import settings
from demosys.resources import shaders

settings.add_shader_dir(os.path.join(os.path.dirname(__file__), 'shaders'))


class MeshShader:

    def __init__(self, shader=None, **kwargs):
        self.shader = shader
        self.ctx = context.ctx()

    def draw(self, mesh, projection_matrix=None, view_matrix=None, camera_matrix=None, time=0):
        """
        Draw code for the mesh. Should be overriden.

        :param projection_matrix: projection_matrix (bytes)
        :param view_matrix: view_matrix (bytes)
        :param camera_matrix: camera_matrix (bytes)
        :param time: The current time
        """
        self.shader.uniform("m_proj", projection_matrix)
        self.shader.uniform("m_mv", view_matrix)
        mesh.vao.draw(self.shader)

    def apply(self, mesh):
        """
        Determine if this MeshShader should be applied to the mesh
        Can return self or some MeshShader instance to support dynamic MeshShader creation

        :param mesh: The mesh to inspect
        """
        raise NotImplementedError("apply is not implemented. Please override the MeshShader method")


class ColorShader(MeshShader):
    """
    Simple color shader
    """
    def __init__(self, shader=None, **kwargs):
        super().__init__(shader=shaders.load("scene_default/color.glsl"))

    def draw(self, mesh, projection_matrix=None, view_matrix=None, camera_matrix=None, time=0):

        if mesh.material:
            # if mesh.material.double_sided:
            #     self.ctx.disable(moderngl.CULL_FACE)
            # else:
            #     self.ctx.enable(moderngl.CULL_FACE)

            if mesh.material.color:
                self.shader.uniform("color", tuple(mesh.material.color))
            else:
                self.shader.uniform("color", (1.0, 1.0, 1.0, 1.0))

        self.shader.uniform("m_proj", projection_matrix)
        self.shader.uniform("m_view", view_matrix)
        self.shader.uniform("m_cam", camera_matrix)
        mesh.vao.draw(self.shader)

    def apply(self, mesh):
        if not mesh.material:
            return None

        if not mesh.attributes.get("NORMAL"):
            return None

        if mesh.material.mat_texture is None:
            return self

        return None


class TextureShader(MeshShader):
    """
    Simple texture shader
    """
    def __init__(self, shader=None, **kwargs):
        super().__init__(shader=shaders.load("scene_default/texture.glsl"))

    def draw(self, mesh, projection_matrix=None, view_matrix=None, camera_matrix=None, time=0):
        # if mesh.material.double_sided:
        #     self.ctx.disable(moderngl.CULL_FACE)
        # else:
        #     self.ctx.enable(moderngl.CULL_FACE)

        mesh.material.mat_texture.texture.use()
        self.shader.uniform("texture0", 0)
        self.shader.uniform("m_proj", projection_matrix)
        self.shader.uniform("m_view", view_matrix)
        self.shader.uniform("m_cam", camera_matrix)
        mesh.vao.draw(self.shader)

    def apply(self, mesh):
        if not mesh.material:
            return None

        if not mesh.attributes.get("NORMAL"):
            return None

        if mesh.material.mat_texture is not None:
            return self

        return None


class FallbackShader(MeshShader):
    """
    Fallback shader only rendering positions in white
    """
    def __init__(self, shader=None, **kwargs):
        super().__init__(shader=shaders.load("scene_default/fallback.glsl"))

    def draw(self, mesh, projection_matrix=None, view_matrix=None, camera_matrix=None, time=0):

        self.shader.uniform("m_proj", projection_matrix)
        self.shader.uniform("m_view", view_matrix)
        self.shader.uniform("m_cam", camera_matrix)

        if mesh.material:
            self.shader.uniform("color", tuple(mesh.material.color[0:3]))
        else:
            self.shader.uniform("color", (1.0, 1.0, 1.0))

        mesh.vao.draw(self.shader)

    def apply(self, mesh):
        return self
