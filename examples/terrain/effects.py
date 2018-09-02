import math
import moderngl

from demosys.effects import effect
from demosys import geometry
from pyrr import matrix44


def calculate_triangles(n: int):
    """
    Calculate the number of triangles for the barycentric subdivision of a
    single triangle (where the inner and outer subdivision is equal
    """
    if n < 0:
        return 1
    if n == 0:
        return 0
    return ((2 * n -2) * 3) + calculate_triangles(n - 2)


class TerrainTessellation(effect.Effect):

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
        self.tess_level = 64

        original_triangles = 8 * 8 * 2
        tess_triangles = calculate_triangles(self.tess_level)
        print("Number of triangles:", original_triangles)
        print("Total triangles with tessellation:", original_triangles * tess_triangles)

    def draw(self, time, frametime, target):
        self.ctx.enable_only(moderngl.DEPTH_TEST)

        m_proj = self.create_projection(near=0.1, far=800.0)
        m_mv = self.create_transformation(translation=(0.0, -20.0, -200.0))
        m_mv = matrix44.multiply(m_mv, self.sys_camera.view_matrix)

        self.ctx.patch_vertices = 3
        self.ctx.wireframe = True if math.fmod(time, 10) < 5.0 else False

        self.heightmap.use(location=0)
        self.heights.value = 0
        self.proj_matrix.write(m_proj.astype('f4').tobytes())
        self.mv_matrix.write(m_mv.astype('f4').tobytes())

        self.program['TessLevelInner'].value = self.tess_level
        self.program['TessLevelOuter'].value = self.tess_level

        self.terrain.render(self.program, mode=moderngl.PATCHES)
