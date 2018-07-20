import moderngl as mgl
# import math
from demosys.effects import effect
from demosys import geometry
from demosys.opengl import FBO


class GeoCubesEffect(effect.Effect):
    """Simple effect drawing a textured cube"""
    def __init__(self):
        self.cube_shader1 = self.get_shader('geocubes/cube_multi_fade.glsl')
        self.cube_shader2 = self.get_shader('geocubes/cube_texture_light.glsl')
        self.quad_shader = self.get_shader('geocubes/quad_fs_uvscale.glsl')

        self.texture1 = self.get_texture('geocubes/texture.png')
        self.texture2 = self.get_texture('geocubes/GreenFabric.png')

        self.cube = geometry.cube(4.0, 4.0, 4.0)

        axis_range = 100.0
        range_tuple = (-axis_range, axis_range)

        self.points = geometry.points_random_3d(
            50_000,
            range_x=range_tuple,
            range_y=range_tuple,
            range_z=range_tuple,
            seed=7656456
        )
        self.quad = geometry.quad_fs()
        self.fbo = FBO.create((512, 512), depth=True)

    @effect.bind_target
    def draw(self, time, frametime, target):
        self.ctx.enable(mgl.DEPTH_TEST)
        self.ctx.enable(mgl.CULL_FACE)

        mv_m = self.create_transformation(rotation=(time * 1.2, time * 2.1, time * 0.25),
                                          translation=(0.0, 0.0, -8.0))
        normal_m = self.create_normal_matrix(mv_m)
        proj_m = self.create_projection(fov=60.0, ratio=1.0)

        with self.fbo:
            self.cube_shader1.uniform("m_proj", proj_m.astype('f4').tobytes())
            self.cube_shader1.uniform("m_mv", mv_m.astype('f4').tobytes())
            self.cube_shader1.uniform("m_normal", normal_m.astype('f4').tobytes())
            self.texture1.use(location=0)
            self.texture2.use(location=1)
            self.cube_shader1.uniform("texture0", 0)
            self.cube_shader1.uniform("texture1", 1)
            self.cube_shader1.uniform("time", time)
            self.cube.draw(self.cube_shader1)

        self.sys_camera.projection.update(fov=75, near=0.1, far=1000)

        view_m = self.sys_camera.view_matrix
        normal_m = self.create_normal_matrix(view_m)

        self.cube_shader2.uniform("m_proj", self.sys_camera.projection.tobytes())
        self.cube_shader2.uniform("m_mv", view_m.astype('f4').tobytes())
        self.cube_shader2.uniform("m_normal", normal_m.astype('f4').tobytes())
        self.fbo.color_buffers[0].use(location=0)
        self.cube_shader2.uniform("texture0", 0)
        self.cube_shader2.uniform("time", time)
        self.cube_shader2.uniform("lightpos", (0.0, 0.0, 0.0))
        self.points.draw(self.cube_shader2)

        self.fbo.clear(red=0.5, green=0.5, blue=0.5, alpha=1.0, depth=1.0)
