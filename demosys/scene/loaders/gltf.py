# Spec: https://github.com/KhronosGroup/glTF/blob/master/specification/2.0/README.md#asset

import json
import numpy
import os

from OpenGL import GL
from OpenGL.arrays.vbo import VBO

from pyrr import matrix44, Matrix44

from demosys.opengl import VAO
from demosys.opengl.constants import TYPE_INFO
from demosys.scene import (
    Node,
    Mesh,
    Material,
)

# Supported buffer targets
BUFFER_TARGETS = {
    34962: "GL_ARRAY_BUFFER",
    34963: "GL_ELEMENT_ARRAY_BUFFER",
}

# numpy dtype mapping
NP_COMPONENT_DTYPE = {
    5121: numpy.dtype(numpy.uint8),
    5123: numpy.dtype(numpy.uint16),
    5126: numpy.dtype(numpy.float32),
}

ACCESSOR_TYPE = {
    "SCALAR": 1,
    "VEC2": 2,
    "VEC3": 3,
    "VEC4": 4,
}


class GLTF2:
    """
    Represents a GLTF 2.0 file
    """
    def __init__(self, file_path):
        """
        Parse the json file and validate its contents.
        No actual data loading will happen.

        Supported formats:
        - gltf json format with external resources
        - gltf embedded buffers
        - glb Binary format
        """
        self.scenes = []
        self.nodes = []
        self.meshes = []
        self.materials = []

        self.meta = None
        self.file = file_path
        self.path = ""
        self.scene = None

    def load(self, scene, file=None):
        """
        Deferred loading of the scene

        :param scene: The scene object
        :param file: Resolved path if changed by finder
        """
        print("Loading", self.file)
        self.scene = scene
        if file:
            self.file = file
        self.path = os.path.dirname(self.file)

        # Load gltf json file
        if self.file.endswith('.gltf'):
            self.load_gltf()

        # Load binary gltf file
        if self.file.endswith('.glb'):
            self.load_glb()

        self.meta.check_version()
        self.load_images()
        self.load_meshes()
        self.load_materials()
        self.load_nodes()

    def load_gltf(self):
        """Loads a gltf json file"""
        with open(self.file) as fd:
            self.meta = GLTFMeta(self.file, json.load(fd))

    def load_glb(self):
        """Loads a binary gltf file"""
        pass

    def load_images(self):
        for image in self.meta.images:
            pass

    def load_meshes(self):
        for mesh in self.meta.meshes:
            m = mesh.load()
            self.meshes.append(m)

    def load_materials(self):
        # Create material objects
        for mat in self.meta.materials:
            m = Material(mat.name)
            m.color = mat.baseColorFactor
            self.materials.append(m)

        # Map to meshes
        for i, mesh in enumerate(self.meta.meshes):
            self.meshes[i].material = self.materials[mesh.primitives[0].material]

    def load_nodes(self):
        # Start with root nodes in the scene
        for node_id in self.meta.scenes[0].nodes:
            node = self.load_node(self.meta.nodes[node_id])
            self.scene.add_node(node)

    def load_node(self, meta, parent=None):
        # Create the node
        node = Node()

        if meta.matrix is not None:
            node.matrix = Matrix44(value=meta.matrix)

        # FIXME: check for quaternions

        if meta.mesh is not None:
            node.mesh = self.meshes[meta.mesh]

        if meta.camera is not None:
            # FIXME: Use a proper camera class
            node.camera = self.meta.cameras[meta.camera]

        if parent:
            parent.add_child(node)

        # Follow children
        if meta.has_children:
            for node_id in meta.children:
                self.load_node(self.meta.nodes[node_id], parent=node)

        return node


class GLTFMeta:
    """Container for gltf metadata"""
    def __init__(self, file, data):
        self.file = file
        self.path = os.path.dirname(self.file)
        self.asset = GLTFAsset(data['asset'])
        self.materials = [GLTFMaterial(m) for m in data['materials']] if data.get('materials') else []
        self.images = [GLTFImage(i) for i in data['images']] if data.get('images') else []
        self.samplers = [GLTFSampler(s) for s in data['samplers']] if data.get('samplers') else []
        self.textures = [GLTFTexture(t) for t in data['textures']] if data.get('textures') else []
        self.scenes = [GLTFScene(s) for s in data['scenes']] if data.get('scenes') else []
        self.nodes = [GLTFNode(n) for n in data['nodes']] if data.get('nodes') else []
        self.meshes = [GLTFMesh(m) for m in data['meshes']] if data.get('meshes') else []
        self.cameras = [GLTFCamera(c) for c in data['cameras']] if data.get('cameras') else []
        self.bufferViews = [GLTFBufferView(v) for v in data['bufferViews']] if data.get('bufferViews') else []
        self.buffers = [GLTFBuffer(b, self.path) for b in data['buffers']] if data.get('buffers') else []
        self.accessors = [GLTFAccessor(a) for a in data['accessors']] if data.get('accessors') else []

        self._link_data()

        self.buffers_exist()
        self.images_exist()

    def _link_data(self):
        """Add references"""
        # accessors -> bufferViews -> buffers
        for acc in self.accessors:
            acc.bufferView = self.bufferViews[acc.bufferViewId]
        for bv in self.bufferViews:
            bv.buffer = self.buffers[bv.bufferId]

        # Meshes
        for mesh in self.meshes:
            for p in mesh.primitives:
                p.indices = self.accessors[p.indices]
                for name, value in p.attributes.items():
                    p.attributes[name] = self.accessors[value]

    @property
    def version(self):
        return self.asset.version

    def check_version(self, required='2.0'):
        if not self.version == required:
            msg = "GLTF Format version is not 2.0. Version states '{}' in file {}".format(
                self.version,
                self.file
            )
            raise ValueError(msg)

    def buffers_exist(self):
        """Checks if the bin files referenced exist"""
        for buff in self.buffers:
            path = os.path.join(self.path, buff.uri)
            if not os.path.exists(path):
                raise FileNotFoundError("Buffer %s referenced in %s not found", path, self.file)

    def images_exist(self):
        """checks if the images references in textures exist"""
        pass


class GLTFAsset:
    """Asset Information"""
    def __init__(self, data):
        self.version = data.get('version')
        self.generator = data.get('generator')
        self.copyright = data.get('copyright')


class GLTFMesh:

    def __init__(self, data):
        class Primitives:
            def __init__(self, data):
                self.attributes = data.get('attributes')
                self.indices = data.get('indices')
                self.mode = data.get('mode')
                self.material = data.get('material')

        self.name = data.get('name')
        self.primitives = [Primitives(p) for p in data.get('primitives')]

    def load(self):
        component_type, index_vbo = self.load_indices()
        attribs = self.load_attributes()

        name_map = {
            'POSITION': 'in_position',
            'NORMAL': 'in_normal',
            'TEXCOORD_0': 'in_uv',
            'TANGENT': 'in_tangent',
            'JOINTS_0': 'in_joints',
            'WEIGHTS_0': 'in_heights',
        }

        vao = VAO(self.name, mode=self.primitives[0].mode or GL.GL_TRIANGLES)
        vao.set_element_buffer(component_type.value, index_vbo)
        for name, components, component_type, vbo in attribs:
            vao.add_array_buffer(component_type.value, vbo)
            vao.map_buffer(vbo, name_map[name], components)

        vao.build()
        return Mesh(self.name, vao=vao)

    def load_indices(self):
        """Loads the index buffer / polygon list"""
        _, component_type, vbo = self.primitives[0].indices.read(target=GL.GL_ELEMENT_ARRAY_BUFFER)
        # print("vbo", vbo.__dict__)
        return component_type, vbo

    def load_attributes(self):
        # figure out what buffers are interleaved
        attribs = []
        for name, accessor in self.primitives[0].attributes.items():
            components, component_type, vbo = accessor.read(target=GL.GL_ARRAY_BUFFER)
            attribs.append((name, components, component_type, vbo))

        return attribs

    def is_interleaved(self):
        pass

    def get_bbox(self):
        """Get the bounding box for the mesh"""
        accessor = self.primitives[0].attributes.get('POSITION')
        return accessor.min, accessor.max


class GLTFAccessor:
    def __init__(self, data):
        self.bufferViewId = data.get('bufferView')
        self.bufferView = None
        self.byteOffset = data.get('byteOffset') or 0
        self.componentType = TYPE_INFO[data['componentType']]
        self.count = data.get('count')
        self.max = data.get('max')
        self.min = data.get('min')
        self.type = data.get('type')

    def read(self, target=None):
        """
        Reads buffer data
        :return: component count, component type, data
        """
        # ComponentType helps us determine the datatype
        dtype = NP_COMPONENT_DTYPE[self.componentType.value]
        return ACCESSOR_TYPE[self.type], self.componentType, self.bufferView.read(
            target=target,
            byte_offset=self.byteOffset,
            dtype=dtype,
            count=self.count * ACCESSOR_TYPE[self.type],
        )


class GLTFBufferView:
    def __init__(self, data):
        self.bufferId = data.get('buffer')
        self.buffer = None
        self.byteOffset = data.get('byteOffset') or 0
        self.byteLength = data.get('byteLength')
        self.byteStride = data.get('byteStride') or 0
        # Valid: 34962 (ARRAY_BUFFER) and 34963 (ELEMENT_ARRAY_BUFFER) or None
        self.target = data.get('target')

    def read(self, byte_offset=0, dtype=None, count=0, target=None):
        data = self.buffer.read(
            byte_offset=byte_offset + self.byteOffset,
            byte_length=self.byteLength,
        )
        vbo = VBO(numpy.frombuffer(data, count=count, dtype=dtype),
                  target=BUFFER_TARGETS[target])
        return vbo


class GLTFBuffer:
    def __init__(self, data, path):
        self.path = path
        self.byteLength = data.get('byteLength')
        self.uri = data.get('uri')
        self.data = None

    @property
    def has_data_uri(self):
        return self.uri.startswith("data:")

    def open(self):
        if self.data:
            return

        if self.has_data_uri:
            raise NotImplemented("data-uri resource loading not implemented")

        with open(os.path.join(self.path, self.uri), 'rb') as fd:
            self.data = fd.read()

    def read(self, byte_offset=0, byte_length=0):
        self.open()
        return self.data[byte_offset:byte_offset + byte_length]


class GLTFScene:
    def __init__(self, data):
        self.nodes = data['nodes']


class GLTFNode:
    def __init__(self, data):
        self.children = data.get('children')
        self.matrix = data.get('matrix')
        self.mesh = data.get('mesh')
        self.camera = data.get('camera')

        self.translation = data.get('translation')
        self.rotation = data.get('rotation')
        self.scale = data.get('scale')

        if self.translation is not None:
            self.matrix = matrix44.create_from_translation(self.translation)

    @property
    def has_children(self):
        return self.children is not None and len(self.children) > 0

    @property
    def is_resource_node(self):
        """Is this just a reference node to a resource?"""
        return self.camera is not None or self.mesh is not None


class GLTFMaterial:
    def __init__(self, data):
        self.name = data.get('name')
        self.baseColorFactor = None
        self.metallicFactor = None
        self.emissiveFactor = None

        pbr = data.get('pbrMetallicRoughness')
        if pbr:
            self.baseColorFactor = pbr.get('baseColorFactor')
            self.metallicFactor = pbr.get('metallicFactor')

        self.emissiveFactor = data.get('emissiveFactor')


class GLTFImage:
    def __init__(self, data):
        self.uri = data['uri']


class GLTFTexture:
    def __init__(self, data):
        self.sampler = data.get('sampler')
        self.source = data.get('source')


class GLTFSampler:
    def __init__(self, data):
        self.magFilter = data.get('magFilter')
        self.minFilter = data.get('minFilter')
        self.wrapS = data.get('wrapS')
        self.wrapT = data.get('wrapT')


class GLTFCamera:
    def __init__(self, data):
        self.data = data
        # "perspective": {
        #     "aspectRatio": 1.0,
        #     "yfov": 0.266482561826706,
        #     "zfar": 1000000.0,
        #     "znear": 0.04999999701976776
        # },
        # "type": "perspective"
