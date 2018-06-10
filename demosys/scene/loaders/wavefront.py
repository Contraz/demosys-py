import numpy
from .base import SceneLoader
import pywavefront

from OpenGL import GL
from OpenGL.arrays.vbo import VBO
from demosys.opengl import VAO
from demosys.scene import Mesh, Node, Material, MaterialTexture
from demosys.resources import textures
from demosys.opengl import samplers


class ObjLoader(SceneLoader):
    """Loade obj files"""
    file_extensions = ['.obj', '.obj.gz']

    def __init__(self, file_path):
        super().__init__(file_path)

    def load(self, scene, file=None):
        """Deferred loading"""
        data = pywavefront.Wavefront(file)

        for name, mat in data.materials.items():
            vbo = VBO(numpy.array(mat.vertices, dtype=numpy.dtype(numpy.float32)))

            vao = VAO(mat.name, mode=GL.GL_TRIANGLES)
            vao.add_array_buffer(GL.GL_FLOAT, vbo)
            mesh = Mesh(mat.name, vao=vao)

            if "T2F" in mat.vertex_format:
                vao.map_buffer(vbo, "in_uv", 2)
                mesh.add_attribute("TEXCOORD_0", "in_uv", 2)

            if "N3F" in mat.vertex_format:
                vao.map_buffer(vbo, "in_normal", 3)
                mesh.add_attribute("NORMAL", "in_normal", 3)

            vao.map_buffer(vbo, "in_position", 3)
            mesh.add_attribute("POSITION", "in_position", 3)

            vao.build()

            scene.meshes.append(mesh)

            mesh.material = Material(mat.name)
            mesh.material.color = mat.diffuse
            if mat.texture:
                mesh.material.mat_texture = MaterialTexture(
                    texture=textures.get(mat.texture.image_name, create=True, mipmap=True),
                    sampler=samplers.create_sampler(wrap_s=GL.GL_CLAMP_TO_EDGE,
                                                    wrap_t=GL.GL_CLAMP_TO_EDGE)
                )

            node = Node(mesh=mesh)
            scene.root_nodes.append(node)

        return scene
