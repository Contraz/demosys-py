from demosys.effects import effect
from demosys.opengl import geometry, FBO
# from pyrr import matrix44, Vector3, Matrix33
from OpenGL import GL


class CubeEffect(effect.Effect):
    """Simple effect drawing a textured cube"""
    depth_testing = True

    def __init__(self):
        self.cube_shader1 = self.get_shader('cube/cube_multi_fade.glsl')
        self.cube_shader2 = self.get_shader('cube/cube_texture_light.glsl')
        self.quad_shader = self.get_shader('quad_fs_uvscale.glsl')
        self.texture1 = self.get_texture('cube/texture.png')
        self.texture2 = self.get_texture('cube/GreenFabric.png')
        self.cube = geometry.cube(4.0, 4.0, 4.0)
        r = (-25.0, 25.0)
        self.points = geometry.points_random_3d(1000, range_x=r, range_y=r, range_z=r, seed=7656456)
        self.quad = geometry.quad_fs()
        self.fbo = FBO.create(512, 512, depth=True)

    @effect.bind_target
    def draw(self, time, target):
        time *= 0.5
        target.bind()
        GL.glEnable(GL.GL_DEPTH_TEST)
        self.fbo.bind()

        mv_m = self.create_transformation(rotation=(time * 1.2, time * 2.1, time * 0.25),
                                          translation=(0.0, 0.0, -8.0))
        normal_m = self.create_normal_matrix(mv_m)
        proj_m = self.create_projection(fov=60.0, ratio=1.0)

        self.cube.bind(self.cube_shader1)
        self.cube_shader1.uniform_mat4("ProjM", proj_m)
        self.cube_shader1.uniform_mat4("ModelViewM", mv_m)
        self.cube_shader1.uniform_mat3("NormalM", normal_m)
        self.cube_shader1.uniform_sampler_2d(0, "texture0", self.texture1)
        self.cube_shader1.uniform_sampler_2d(1, "texture1", self.texture2)
        self.cube_shader1.uniform_1f("time", time)
        self.cube.draw()

        self.fbo.release()

        proj_m = self.create_projection(fov=60.0, far=1000)

        self.points.bind(self.cube_shader2)
        self.cube_shader2.uniform_mat4("ProjM", proj_m)
        self.cube_shader2.uniform_mat4("ModelViewM", mv_m)
        self.cube_shader2.uniform_mat3("NormalM", normal_m)
        self.cube_shader2.uniform_sampler_2d(0, "texture0", self.fbo.color_buffers[0])
        self.points.draw(mode=GL.GL_POINTS)

        GL.glClearColor(0.5, 0.5, 0.5, 1)
        self.fbo.clear()
        target.release()
