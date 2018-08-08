import moderngl as mgl
# import math
from demosys.effects import effect
from demosys import geometry


class GeoCubesEffect(effect.Effect):
    """Simple effect drawing a textured cube"""
    def __init__(self):
        self.cube_prog1 = self.get_program('cube_multi_fade')
        self.cube_prog2 = self.get_program('cube_texture_light')
        self.quad_prog = self.get_program('quad_fs_uvscale')

        self.texture1 = self.get_texture('texture')
        self.texture2 = self.get_texture('GreenFabric')

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

        self.fbo = self.ctx.framebuffer(
            self.ctx.texture((512, 512), 4),
            depth_attachment=self.ctx.depth_texture((512, 512)),
        )

    def draw(self, time, frametime, target):
        self.ctx.enable(mgl.DEPTH_TEST)
        self.ctx.enable(mgl.CULL_FACE)

        mv_m = self.create_transformation(rotation=(time * 1.2, time * 2.1, time * 0.25),
                                          translation=(0.0, 0.0, -8.0))
        normal_m = self.create_normal_matrix(mv_m)
        proj_m = self.create_projection(fov=60.0, ratio=1.0)

        self.fbo.use()

        self.cube_prog1.uniform("m_proj", proj_m.astype('f4').tobytes())
        self.cube_prog1.uniform("m_mv", mv_m.astype('f4').tobytes())
        self.cube_prog1.uniform("m_normal", normal_m.astype('f4').tobytes())
        self.texture1.use(location=0)
        self.texture2.use(location=1)
        self.cube_prog1.uniform("texture0", 0)
        self.cube_prog1.uniform("texture1", 1)
        self.cube_prog1.uniform("time", time)
        self.cube.draw(self.cube_prog1)

        target.use()

        self.sys_camera.projection.update(fov=75, near=0.1, far=1000)

        view_m = self.sys_camera.view_matrix
        normal_m = self.create_normal_matrix(view_m)

        self.cube_prog2.uniform("m_proj", self.sys_camera.projection.tobytes())
        self.cube_prog2.uniform("m_mv", view_m.astype('f4').tobytes())
        self.cube_prog2.uniform("m_normal", normal_m.astype('f4').tobytes())
        self.fbo.color_attachments[0].use(location=0)
        self.cube_prog2.uniform("texture0", 0)
        self.cube_prog2.uniform("time", time)
        self.cube_prog2.uniform("lightpos", (0.0, 0.0, 0.0))
        self.points.draw(self.cube_prog2)

        self.fbo.clear(red=0.5, green=0.5, blue=0.5, alpha=1.0, depth=1.0)
