from pathlib import Path

import numpy

import moderngl
import pywavefront
from demosys.opengl import VAO
from demosys.resources import textures
from demosys.scene import Material, MaterialTexture, Mesh, Node
from pywavefront import cache
from pywavefront.obj import ObjParser

from .base import SceneLoader


def translate_buffer_format(vertex_format):
    """Translate the buffer format"""
    buffer_format = []
    attributes = []
    mesh_attributes = []

    if "T2F" in vertex_format:
        buffer_format.append("2f")
        attributes.append("in_uv")
        mesh_attributes.append(("TEXCOORD_0", "in_uv", 2))

    if "C3F" in vertex_format:
        buffer_format.append("3f")
        attributes.append("in_color")
        mesh_attributes.append(("NORMAL", "in_color", 3))

    if "N3F" in vertex_format:
        buffer_format.append("3f")
        attributes.append("in_normal")
        mesh_attributes.append(("NORMAL", "in_normal", 3))

    buffer_format.append("3f")
    attributes.append("in_position")
    mesh_attributes.append(("POSITION", "in_position", 3))

    return " ".join(buffer_format), attributes, mesh_attributes


class VAOCacheLoader(cache.CacheLoader):
    """Load geometry data directly into vaos"""

    def load_vertex_buffer(self, fd, material, length):
        buffer_format, attributes, mesh_attributes = translate_buffer_format(material.vertex_format)

        vao = VAO(material.name, mode=moderngl.TRIANGLES)
        # buffer = context.ctx().buffer(fd.read(length))
        vao.buffer(fd.read(length), buffer_format, attributes)

        setattr(material, 'vao', vao)
        setattr(material, 'buffer_format', buffer_format)
        setattr(material, 'attributes', attributes)
        setattr(material, 'mesh_attributes', mesh_attributes)


ObjParser.cache_loader_cls = VAOCacheLoader


class ObjLoader(SceneLoader):
    """Loade obj files"""
    file_extensions = [
        ['.obj'],
        ['.obj', '.gz'],
        ['.bin'],
    ]

    def __init__(self, path):
        super().__init__(path)

    def load(self, scene, path: Path=None):
        """Deferred loading"""
        if path.suffix == '.bin':
            path = path.parent / path.stem

        data = pywavefront.Wavefront(str(path), create_materials=True, cache=True)

        for _, mat in data.materials.items():

            mesh = Mesh(mat.name)

            # Traditional loader
            if mat.vertices:
                buffer_format, attributes, mesh_attributes = translate_buffer_format(mat.vertex_format)
                vbo = numpy.array(mat.vertices, dtype='f4')

                vao = VAO(mat.name, mode=moderngl.TRIANGLES)
                vao.buffer(vbo, buffer_format, attributes)
                mesh.vao = vao

                for attrs in mesh_attributes:
                    mesh.add_attribute(*attrs)

            # Binary cache loader
            elif hasattr(mat, 'vao'):
                mesh = Mesh(mat.name)
                mesh.vao = mat.vao
                for attrs in mat.mesh_attributes:
                    mesh.add_attribute(*attrs)
            else:
                # Empty
                continue

            scene.meshes.append(mesh)

            mesh.material = Material(mat.name)
            mesh.material.color = mat.diffuse
            if mat.texture:
                mesh.material.mat_texture = MaterialTexture(
                    texture=textures.get(mat.texture.path, create=True, mipmap=True),
                    # sampler=samplers.create(
                    #     wrap_s=GL.GL_CLAMP_TO_EDGE,
                    #     wrap_t=GL.GL_CLAMP_TO_EDGE,
                    #     anisotropy=8,
                    # )
                )

            node = Node(mesh=mesh)
            scene.root_nodes.append(node)

        return scene
