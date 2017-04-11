# import math
from demosys.effects import effect
from demosys.opengl import geometry, FBO
# from pyrr import Vector3
from OpenGL import GL


class CubeEffect(effect.Effect):
    """Simple effect drawing a textured cube"""
    def init(self):
        self.cube_shader1 = self.get_shader('cube/cube_multi_fade.glsl')
        self.cube_shader2 = self.get_shader('cube/cube_texture_light.glsl')
        self.quad_shader = self.get_shader('quad_fs_uvscale.glsl')
        self.texture1 = self.get_texture('cube/texture.png')
        self.texture2 = self.get_texture('cube/GreenFabric.png')
        self.cube = geometry.cube(4.0, 4.0, 4.0)
        v = 100.0
        r = (-v, v)
        self.points = geometry.points_random_3d(50_000, range_x=r, range_y=r, range_z=r, seed=7656456)
        self.quad = geometry.quad_fs()
        self.fbo = FBO.create(512, 512, depth=True)

    @effect.bind_target
    def draw(self, time, frametime, target):
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_CULL_FACE)

        mv_m = self.create_transformation(rotation=(time * 1.2, time * 2.1, time * 0.25),
                                          translation=(0.0, 0.0, -8.0))
        normal_m = self.create_normal_matrix(mv_m)
        proj_m = self.create_projection(fov=60.0, ratio=1.0)

        with self.fbo:
            with self.cube.bind(self.cube_shader1) as shader:
                shader.uniform_mat4("m_proj", proj_m)
                shader.uniform_mat4("m_mv", mv_m)
                shader.uniform_mat3("m_normal", normal_m)
                shader.uniform_sampler_2d(0, "texture0", self.texture1)
                shader.uniform_sampler_2d(1, "texture1", self.texture2)
                shader.uniform_1f("time", time)
            self.cube.draw()

        # Test camera
        self.sys_camera.set_projection(near=0.1, far=1000)
        # self.sys_camera.set_position(10.0, 0.0, 10.0)
        # self.sys_camera.set_position(math.sin(time) * 10,
        #                                  math.sin(time * 10),
        #                                  math.cos(time) * 10)
        # view_m = self.sys_camera.look_at(pos=[0.0, 0.0, 0.0])
        view_m = self.sys_camera.view_matrix
        normal_m = self.create_normal_matrix(view_m)

        with self.points.bind(self.cube_shader2) as shader:
            shader.uniform_mat4("m_proj", self.sys_camera.projection)
            shader.uniform_mat4("m_mv", view_m)
            shader.uniform_mat3("m_normal", normal_m)
            shader.uniform_sampler_2d(0, "texture0", self.fbo.color_buffers[0])
            shader.uniform_1f("time", time)
            shader.uniform_3f("lightpos", 0.0, 0.0, 0.0)
        self.points.draw(mode=GL.GL_POINTS)

        GL.glClearColor(0.5, 0.5, 0.5, 1)
        self.fbo.clear()
