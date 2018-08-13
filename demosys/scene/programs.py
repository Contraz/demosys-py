import os

from demosys import context
from demosys.conf import settings
from demosys.resources import programs
from demosys.resources.meta import ProgramDescription

settings.add_program_dir(os.path.join(os.path.dirname(__file__), 'programs'))


class MeshProgram:

    def __init__(self, program=None, **kwargs):
        self.program = program
        self.ctx = context.ctx()

    def draw(self, mesh, projection_matrix=None, view_matrix=None, camera_matrix=None, time=0):
        """
        Draw code for the mesh. Should be overriden.

        :param projection_matrix: projection_matrix (bytes)
        :param view_matrix: view_matrix (bytes)
        :param camera_matrix: camera_matrix (bytes)
        :param time: The current time
        """
        self.program["m_proj"].write(projection_matrix)
        self.program["m_mv"].write(view_matrix)
        mesh.vao.render(self.program)

    def apply(self, mesh):
        """
        Determine if this MeshProgram should be applied to the mesh
        Can return self or some MeshProgram instance to support dynamic MeshProgram creation

        :param mesh: The mesh to inspect
        """
        raise NotImplementedError("apply is not implemented. Please override the MeshProgram method")


class ColorProgram(MeshProgram):
    """
    Simple color program
    """
    def __init__(self, program=None, **kwargs):
        super().__init__(program=None)
        self.program = programs.load(ProgramDescription(
            label="scene_default/color.glsl",
            path="scene_default/color.glsl"))

    def draw(self, mesh, projection_matrix=None, view_matrix=None, camera_matrix=None, time=0):

        if mesh.material:
            # if mesh.material.double_sided:
            #     self.ctx.disable(moderngl.CULL_FACE)
            # else:
            #     self.ctx.enable(moderngl.CULL_FACE)

            if mesh.material.color:
                self.program["color"].value = tuple(mesh.material.color)
            else:
                self.program["color"].value = (1.0, 1.0, 1.0, 1.0)

        self.program["m_proj"].write(projection_matrix)
        self.program["m_view"].write(view_matrix)
        self.program["m_cam"].write(camera_matrix)
        mesh.vao.render(self.program)

    def apply(self, mesh):
        if not mesh.material:
            return None

        if not mesh.attributes.get("NORMAL"):
            return None

        if mesh.material.mat_texture is None:
            return self

        return None


class TextureProgram(MeshProgram):
    """
    Simple texture program
    """
    def __init__(self, program=None, **kwargs):
        super().__init__(program=None)
        self.program = programs.load(ProgramDescription(
            label="scene_default/texture.glsl",
            path="scene_default/texture.glsl"))

    def draw(self, mesh, projection_matrix=None, view_matrix=None, camera_matrix=None, time=0):
        # if mesh.material.double_sided:
        #     self.ctx.disable(moderngl.CULL_FACE)
        # else:
        #     self.ctx.enable(moderngl.CULL_FACE)

        mesh.material.mat_texture.texture.use()
        self.program["texture0"].value = 0
        self.program["m_proj"].write(projection_matrix)
        self.program["m_view"].write(view_matrix)
        self.program["m_cam"].write(camera_matrix)
        mesh.vao.render(self.program)

    def apply(self, mesh):
        if not mesh.material:
            return None

        if not mesh.attributes.get("NORMAL"):
            return None

        if mesh.material.mat_texture is not None:
            return self

        return None


class FallbackProgram(MeshProgram):
    """
    Fallback program only rendering positions in white
    """
    def __init__(self, program=None, **kwargs):
        super().__init__(program=None)
        self.program = programs.load(ProgramDescription(
            label="scene_default/fallback.glsl",
            path="scene_default/fallback.glsl"))

    def draw(self, mesh, projection_matrix=None, view_matrix=None, camera_matrix=None, time=0):

        self.program["m_proj"].write(projection_matrix)
        self.program["m_view"].write(view_matrix)
        self.program["m_cam"].write(camera_matrix)

        if mesh.material:
            self.program["color"].value = tuple(mesh.material.color[0:3])
        else:
            self.program["color"].value = (1.0, 1.0, 1.0)

        mesh.vao.render(self.program)

    def apply(self, mesh):
        return self
