from demosys.test import DemosysTestCase
from demosys import resources


class ResourceTestCase(DemosysTestCase):

    def test_stuff(self):
        result = resources.shaders.get('vf_pos.glsl', create=True)
        resources.shaders.load()
