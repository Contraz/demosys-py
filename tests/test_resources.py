import os

import moderngl

from demosys.test import DemosysTestCase
from demosys import resources
from demosys.exceptions import ImproperlyConfigured
from demosys.conf import settings


class ResourceTestCase(DemosysTestCase):

    def test_datafiles(self):
        # string and binary data file
        data_str = self.load_data('data.txt', loader="text")
        data_bin = self.load_data('data.bin', loader="binary")
        self.assertEqual(data_str, '1234')
        self.assertEqual(data_bin, b'\x01\x02\x03\x04')

        with self.assertRaises(ImproperlyConfigured):
            self.load_data('notfound.bin')

    def test_scene(self):
        scene_obj = self.load_scene('cube.obj')
        self.assertEqual(len(scene_obj.nodes), 0)
        self.assertEqual(len(scene_obj.root_nodes), 1)

        scene_gltf = self.load_scene('BoxTextured/glTF/BoxTextured.gltf')
        self.assertEqual(len(scene_gltf.nodes), 2)
        self.assertEqual(len(scene_gltf.root_nodes), 1)

        with self.assertRaises(ValueError):
            self.load_scene('notfound.gltf')

    def test_programs(self):
        program = self.load_program('vf_pos.glsl')
        self.assertIsInstance(program, moderngl.Program)

        # TODO: Test ReloadableProgram here
        # ...

        with self.assertRaises(ValueError):
            self.load_program('notfound.glsl')

    def test_textures(self):
        texture = self.load_texture('wood.jpg')
        self.assertIsInstance(texture, moderngl.Texture)

        with self.assertRaises(ValueError):
            self.load_texture('notfound.png')

    def test_resource_override(self):
        data = self.load_data('data.txt', loader='text')
        self.assertEqual(data, "1234")

        # Add another data directory containing overriding file
        test_root = os.path.dirname(os.path.abspath(__file__))
        settings.add_data_dir(os.path.join(test_root, 'resources', 'data_override'))

        data = self.load_data('data.txt', loader='text')
        self.assertEqual(data, "4567")
