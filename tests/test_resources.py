from demosys.test import DemosysTestCase
from demosys import resources
from demosys.core.exceptions import ImproperlyConfigured


class ResourceTestCase(DemosysTestCase):

    def test_datafiles(self):
        """Loading data files"""
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

    # def test_shaders(self):
    #     result = resources.shaders.get('vf_pos.glsl')
    #     resources.shaders.load()
    #     self.assertNotEqual(result.mglo, None)

    # def test_textures(self):
    #     result = resources.textures.get('wood.jpg')
    #     resources.textures.load()
    #     self.assertNotEqual(result.mglo, None)

    # def test_resource_override(self):
    #     pass
