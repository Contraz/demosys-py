import moderngl

from demosys.effects import effect
from demosys import geometry
from pyrr import matrix44


class Empty(effect.Effect):

    def __init__(self):
        self.terrain = geometry.plane_xz(size=(400, 400), resolution=(8, 8))
        self.program = self.get_program("terrain")
        self.heightmap = self.get_texture('heightmap')
        self.heightmap.repeat_x = False
        self.heightmap.repeat_y = False

        # prefetch uniforms
        self.proj_matrix = self.program['m_proj']
        self.mv_matrix = self.program['m_mv']
        self.heights = self.program['heightmap']

        self.sys_camera.velocity = 50.0

    def draw(self, time, frametime, target):
        self.ctx.enable_only(moderngl.DEPTH_TEST)

        m_proj = self.create_projection(near=0.1, far=800.0)
        m_mv = self.create_transformation(translation=(0.0, -20.0, -200.0))
        m_mv = matrix44.multiply(m_mv, self.sys_camera.view_matrix)

        self.ctx.patch_vertices = 3
        # self.ctx.wireframe = True

        self.heightmap.use(location=0)
        self.heights.value = 0
        self.proj_matrix.write(m_proj.astype('f4').tobytes())
        self.mv_matrix.write(m_mv.astype('f4').tobytes())

        tess_level = 64.0
        self.program['TessLevelInner'].value = tess_level
        self.program['TessLevelOuter'].value = tess_level

        self.terrain.render(self.program, mode=moderngl.PATCHES)
