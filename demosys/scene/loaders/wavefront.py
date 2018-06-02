import numpy
from .base import SceneLoader
import pywavefront

from OpenGL import GL
from OpenGL.arrays.vbo import VBO
from demosys.opengl import VAO
from demosys.scene import Mesh, Node


class ObjLoader(SceneLoader):
    """Loade obj files"""
    file_extensions = ['.obj', '.obj.gz']

    def __init__(self, file_path):
        super().__init__(file_path)

    def load(self, scene, file=None):
        """Deferred loading"""
        data = pywavefront.Wavefront(file)

        for mesh in data.mesh_list:
            for mat in mesh.materials:
                vbo = VBO(numpy.array(mat.vertices, dtype=numpy.dtype(numpy.float32)))

                vao = VAO(mesh.name, mode=GL.GL_TRIANGLES)
                vao.add_array_buffer(GL.GL_FLOAT, vbo)
                vao.map_buffer(vbo, "in_uv", 2)
                vao.map_buffer(vbo, "in_normal", 3)
                vao.map_buffer(vbo, "in_position", 3)
                vao.build()

                mesh = Mesh("moo", vao=vao)
                scene.meshes.append(mesh)
                node = Node(mesh=mesh)
                scene.root_nodes.append(node)

        return scene
