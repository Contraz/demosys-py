from pyrr import matrix44

from demosys.test import DemosysTestCase
from demosys import geometry
from demosys.opengl import Projection
from demosys.effects.registry import effects


class DeferredTestCase(DemosysTestCase):
    """Crude test executing deferred code"""

    def setUp(self):
        effects.add_package('demosys.effects.deferred')
        self.project.load()
        self.instance = self.project.create_effect(
            'test',
            'DeferredRenderer',
            self.window.width,
            self.window.height,
        )

    def test_create(self):
        self.instance.add_point_light(position=[0.0, 0.0, 0.0], radius=40.0)

        cube = geometry.cube(width=8.0, height=8.0, depth=8.0)
        geo_shader_color = self.load_program(path="deferred/geometry_color.glsl")
        projection = Projection()

        with self.instance.gbuffer_scope:
            cube.draw(geo_shader_color)

        self.instance.render_lights(
            matrix44.create_identity(dtype='f4'),
            projection,
        )
        self.instance.combine()
        self.instance.clear()
