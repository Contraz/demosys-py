import os

from demosys.test import DemosysTestCase
from demosys import resources
from demosys.exceptions import ImproperlyConfigured
from demosys.conf import settings


class ResourceTestCase(DemosysTestCase):

    def test_datafiles(self):
        resources.data.flush(destroy=True)        

        # string and binary data file
        data_str = resources.data.load('data.txt', mode="text")
        data_bin = resources.data.load('data.bin', mode="binary")
        self.assertEqual(data_str.data, '1234')
        self.assertEqual(data_bin.data, b'\x01\x02\x03\x04')

        # Ensure requesting the same file returns the existing one
        data = resources.data.load('data.txt', mode="text")
        self.assertEqual(data, data_str)
        data = resources.data.load('data.bin', mode="binary")
        self.assertEqual(data, data_bin)
        self.assertEqual(resources.data.count, 2)

        # Delete and destroy
        resources.data.delete(data_str, destroy=True)
        self.assertIsNone(data_str.data)
        self.assertEqual(resources.data.count, 1)
        resources.data.flush(destroy=True)
        self.assertEqual(resources.data.count, 0)

        with self.assertRaises(ImproperlyConfigured):
            resources.data.load('notfound.bin')

    def test_scene(self):
        resources.scenes.flush(destroy=True)

        scene_obj = resources.scenes.load('cube.obj')
        self.assertEqual(len(scene_obj.nodes), 0)
        self.assertEqual(len(scene_obj.root_nodes), 1)

        scene_gltf = resources.scenes.load('BoxTextured/glTF/BoxTextured.gltf')
        self.assertEqual(len(scene_gltf.nodes), 2)
        self.assertEqual(len(scene_gltf.root_nodes), 1)

        # Ensure requesting the same file returns the existing one
        scene = resources.scenes.load('cube.obj')
        self.assertEqual(scene, scene_obj)
        scene = resources.scenes.load('BoxTextured/glTF/BoxTextured.gltf')
        self.assertEqual(scene, scene_gltf)

        self.assertEqual(resources.scenes.count, 2)

        # Delete and destroy
        resources.scenes.delete(scene_obj, destroy=True)
        self.assertEqual(resources.scenes.count, 1)
        resources.scenes.flush(destroy=True)
        self.assertEqual(resources.scenes.count, 0)

        with self.assertRaises(ImproperlyConfigured):
            resources.scenes.load('notfound.gltf')

    def test_shaders(self):
        resources.shaders.flush(destroy=True)

        shader1 = resources.shaders.load('vf_pos.glsl')
        shader2 = resources.shaders.load('vgf_quads.glsl')
        self.assertEqual(resources.shaders.count, 2)

        # Attempt to reload shaders
        resources.shaders.reload()
        self.assertEqual(resources.shaders.count, 2)

        # Ensure requesting the same file returns the existing one
        shader = resources.shaders.load('vf_pos.glsl')
        self.assertEqual(shader, shader1)
        shader = resources.shaders.load('vgf_quads.glsl')
        self.assertEqual(shader, shader2)

        # Delete and destroy
        resources.shaders.delete(shader1, destroy=True)
        self.assertEqual(resources.shaders.count, 1)
        resources.shaders.flush(destroy=True)
        self.assertEqual(resources.shaders.count, 0)

        with self.assertRaises(ImproperlyConfigured):
            resources.shaders.load('notfound.glsl')

    def test_textures(self):
        resources.textures.flush(destroy=True)

        texture1 = resources.textures.load('wood.jpg')
        texture2 = resources.textures.load('crate.jpg')
        self.assertEqual(resources.textures.count, 2)

        # Ensure requesting the same file returns the existing one
        texture = resources.textures.load('wood.jpg')
        self.assertEqual(texture, texture1)
        texture = resources.textures.load('crate.jpg')
        self.assertEqual(texture, texture2)

        # Delete and destroy
        resources.textures.delete(texture1, destroy=True)
        self.assertEqual(resources.textures.count, 1)
        resources.textures.flush(destroy=True)
        self.assertEqual(resources.textures.count, 0)

        with self.assertRaises(ImproperlyConfigured):
            resources.textures.load('notfound.png')

    def test_resource_override(self):
        data = resources.data.load('data.txt', mode='text')
        self.assertEqual(data.data, "1234")

        # Add another data directory containing overriding file
        test_root = os.path.dirname(os.path.abspath(__file__))
        settings.add_data_dir(os.path.join(test_root, 'resources', 'data_override'))

        resources.data.flush(destroy=True)
        data = resources.data.load('data.txt', mode='text')
        self.assertEqual(data.data, "4567")
