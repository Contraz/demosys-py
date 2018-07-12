from demosys.test import DemosysTestCase
from demosys.opengl import Projection


class ProjectionTest(DemosysTestCase):

    def test_create(self):
        proj = Projection(fov=60, near=0.1, far=10)
        proj.update(fov=75, near=1, far=100)
        proj.tobytes()
        proj.projection_constants
