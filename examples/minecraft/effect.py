import math
import moderngl
from demosys.effects import effect
from demosys.scene import MeshShader
from demosys.opengl import FBO
from pyrr import matrix44




class SimpleCubeEffect(effect.Effect):
    """Generated default effect"""
    def __init__(self):
        self.shader = MinecraftShader(shader=self.get_shader('minecraft.glsl', local=True))
        self.scene = self.get_scene(
            'lost-empire/lost_empire.obj',
            local=True,
            mesh_shaders=[self.shader],
        )
        self.fbo = FBO.create((self.window_width, self.window_height), depth=True)

        self.sampler = self.ctx.sampler()
        self.sampler.filter = moderngl.NEAREST, moderngl.NEAREST

    @effect.bind_target
    def draw(self, time, frametime, target):
        self.ctx.enable(moderngl.DEPTH_TEST)
        self.ctx.disable(moderngl.CULL_FACE)
        self.sys_camera.velocity = 10.0

        m_view = self.create_transformation(translation=(0.0, -5.0, -8.0))
        m_proj = self.create_projection(75, near=0.1, far=300.0)
        m_normal = self.create_normal_matrix(matrix44.multiply(m_view, self.sys_camera.view_matrix))

        with self.fbo:

            if math.fmod(time, 2.0) < 1.0:
                self.sampler.anisotropy = 0.0
                # self.sampler.filter = moderngl.NEAREST, moderngl.NEAREST
            else:
                self.sampler.anisotropy = 16.0
                # self.sampler.filter = moderngl.LINEAR, moderngl.LINEAR

            self.sampler.use(location=0)
            self.scene.draw(m_proj, m_view, self.sys_camera.view_matrix, m_normal, time=time)

        self.ctx.disable(moderngl.DEPTH_TEST)

        self.fbo.draw_color_layer(0)
        self.fbo.draw_depth(0.1, 300, pos=(1.25, 1.25), scale=(0.5, 0.5))
        self.fbo.clear()

class MinecraftShader(MeshShader):
    """
    Simple texture shader
    """
    def __init__(self, shader=None, **kwargs):
        super().__init__(shader=shader)

    def draw(self, mesh, proj_mat, view_mat, cam_mat, normal_mat, time=0):
        mesh.material.mat_texture.texture.use()
        self.shader.uniform("texture0", 0)

        self.shader.uniform("m_proj", proj_mat.astype('f4').tobytes())
        self.shader.uniform("m_view", view_mat.astype('f4').tobytes())
        self.shader.uniform("m_cam", cam_mat.astype('f4').tobytes())
        self.shader.uniform("m_normal", normal_mat.astype('f4').tobytes())

        mesh.vao.draw(self.shader)

    def apply(self, mesh):
        if not mesh.material:
            return None

        if not mesh.attributes.get("NORMAL"):
            return None

        if mesh.material.mat_texture is not None:
            return self

        return None
