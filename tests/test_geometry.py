import pytest

from demosys import geometry
from demosys.test import DemosysTestCase


class GeometryTest(DemosysTestCase):

    def setUp(self):
        self.shader = self.create_shader(path="vf_pos.glsl")

    def test_bbox(self):
        vao = geometry.bbox()
        vao.draw(self.shader)
 
    def test_cube(self):
        vao = geometry.cube(1.0, 1.0, 1.0)
        vao.draw(self.shader)
    
    def test_plane(self):
        vao = geometry.plane_xz()
        vao.draw(self.shader)
    
    def test_points(self):
        vao = geometry.points_random_3d(1000)
        vao.draw(self.shader)

    def test_quad(self):
        vao = geometry.quad_fs()
        vao.draw(self.shader)

    def test_sphere(self):
        vao = geometry.sphere()
        vao.draw(self.shader)
