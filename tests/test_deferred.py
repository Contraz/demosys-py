from pyrr import matrix44

from demosys.test import DemosysTestCase
from demosys.deferred import DeferredRenderer
from demosys import geometry
from demosys.opengl import Projection
from demosys.opengl import texture


class DeferredTestCase(DemosysTestCase):
    """Crude test executing deferred code"""

    def setUp(self):
        texture._init_texture2d_draw()
        texture._init_depth_texture_draw()

    def test_create(self):
        renderer = DeferredRenderer(self.window.width, self.window.height)
        renderer.add_point_light(position=[0.0, 0.0, 0.0], radius=40.0)

        cube = geometry.cube(width=8.0, height=8.0, depth=8.0)
        geo_shader_color = self.create_shader(path="deferred/geometry_color.glsl")
        projection = Projection()

        with renderer.gbuffer_scope:
            cube.draw(geo_shader_color)

        renderer.render_lights(
            matrix44.create_identity(dtype='f4'),
            projection,
        )
        renderer.combine()
        renderer.clear()
