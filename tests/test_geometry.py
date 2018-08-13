from demosys import geometry
from demosys.test import DemosysTestCase


class GeometryTest(DemosysTestCase):
    program = None

    def setUp(self):
        if not getattr(self, 'program'):
            self.program = self.load_program(path="vf_pos.glsl")

    def test_bbox(self):
        vao = geometry.bbox()
        vao.render(self.program)

    def test_cube(self):
        vao = geometry.cube(1.0, 1.0, 1.0)
        vao.render(self.program)

    def test_plane(self):
        vao = geometry.plane_xz()
        vao.render(self.program)

    def test_points(self):
        vao = geometry.points_random_3d(1000)
        vao.render(self.program)

    def test_quad(self):
        vao = geometry.quad_fs()
        vao.render(self.program)

    def test_sphere(self):
        vao = geometry.sphere()
        vao.render(self.program)
