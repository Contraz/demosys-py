import math
from demosys.effects import effect
from demosys.opengl import geometry, FBO
# from pyrr import Vector3
from OpenGL import GL


class CubeEffect(effect.Effect):
    """Simple effect drawing a textured cube"""
    depth_testing = True

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
    def draw(self, time, target):
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

        # Test camera
        self.sys_camera.set_projection(near=0.1, far=1000)
        # self.sys_camera.set_position(10.0, 0.0, 10.0)
        # self.sys_camera.set_position(math.sin(time) * 10,
        #                                  math.sin(time * 10),
        #                                  math.cos(time) * 10)
        # view_m = self.sys_camera.look_at(pos=[0.0, 0.0, 0.0])
        view_m = self.sys_camera.view_matrix
        normal_m = self.create_normal_matrix(view_m)

        self.points.bind(self.cube_shader2)
        self.cube_shader2.uniform_mat4("ProjM", self.sys_camera.projection)
        self.cube_shader2.uniform_mat4("ModelViewM", view_m)
        self.cube_shader2.uniform_mat3("NormalM", normal_m)
        self.cube_shader2.uniform_sampler_2d(0, "texture0", self.fbo.color_buffers[0])
        self.cube_shader2.uniform_1f("time", time)
        self.cube_shader2.uniform_3f("lightpos", 0.0, 0.0, 0.0)
        self.points.draw(mode=GL.GL_POINTS)

        GL.glClearColor(0.5, 0.5, 0.5, 1)
        self.fbo.clear()
