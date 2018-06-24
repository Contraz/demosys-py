import numpy
from .base import SceneLoader
import pywavefront

from OpenGL import GL
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
        data = pywavefront.Wavefront(file, create_materials=True)

        for name, mat in data.materials.items():

            if not mat.vertices:
                continue

            vbo = numpy.array(mat.vertices, dtype=numpy.float32)

            vao = VAO(mat.name, mode=GL.GL_TRIANGLES)
            mesh = Mesh(mat.name)

            # Order: T2F, C3F, N3F and V3F
            buffer_format = []
            attributes = []

            if "T2F" in mat.vertex_format:
                buffer_format.append("2f")
                attributes.append("in_uv")
                mesh.add_attribute("TEXCOORD_0", "in_uv", 2)

            if "C3F" in mat.vertex_format:
                buffer_format.append("3f")
                attributes.append("in_color")
                mesh.add_attribute("NORMAL", "in_color", 3)

            if "N3F" in mat.vertex_format:
                buffer_format.append("3f")
                attributes.append("in_normal")
                mesh.add_attribute("NORMAL", "in_normal", 3)

            buffer_format.append("3f")
            attributes.append("in_position")
            mesh.add_attribute("POSITION", "in_position", 3)

            vao.buffer(vbo, " ".join(buffer_format), attributes)
            mesh.vao = vao

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
