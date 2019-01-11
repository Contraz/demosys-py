import gzip

import moderngl
import numpy
import trimesh

from demosys.loaders.scene.base import SceneLoader
from demosys.opengl.vao import VAO
from demosys.scene import Material, Mesh, Node, Scene


class STLLoader(SceneLoader):
    file_extensions = [
        ['.stl'],
        ['.stl', '.gz'],
    ]

    def load(self):
        path = self.find_scene(self.meta.path)
        if not path:
            raise ValueError("Scene '{}' not found".format(self.meta.path))

        file_obj = str(path)
        if file_obj.endswith('.gz'):
            file_obj = gzip.GzipFile(file_obj)

        stl_mesh = trimesh.load(file_obj, file_type='stl')
        scene = Scene(self.meta.resolved_path)
        scene_mesh = Mesh("mesh")
        scene_mesh.material = Material("default")

        vao = VAO("mesh", mode=moderngl.TRIANGLES)
        vao.buffer(numpy.array(stl_mesh.vertices, dtype='f4'), '3f', ['in_position'])
        vao.buffer(numpy.array(stl_mesh.vertex_normals, dtype='f4'), '3f', ['in_normal'])
        vao.index_buffer(numpy.array(stl_mesh.faces, dtype='u4'))
        scene_mesh.vao = vao
        scene_mesh.add_attribute('POSITION', 'in_position', 3)
        scene_mesh.add_attribute('NORMAL', 'in_normal', 3)

        scene.meshes.append(scene_mesh)
        scene.root_nodes.append(Node(mesh=scene_mesh))
        scene.prepare()

        return scene
