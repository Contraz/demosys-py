# Spec: https://github.com/KhronosGroup/glTF/blob/master/specification/2.0/README.md#asset

import base64
import io
import json
import numpy
import os
import struct

from OpenGL import GL
from OpenGL.arrays.vbo import VBO
from PIL import Image

from pyrr import matrix44, Matrix44, quaternion

from demosys.opengl import VAO
from demosys.opengl import Texture
from demosys.opengl import samplers
from demosys.opengl.constants import TYPE_INFO
from demosys.scene import (
    Node,
    Mesh,
    Material,
    MaterialTexture,
)

GLTF_MAGIC_HEADER = b'glTF'

# Supported buffer targets
BUFFER_TARGETS = {
    34962: "GL_ARRAY_BUFFER",
    34963: "GL_ELEMENT_ARRAY_BUFFER",
}

# numpy dtype mapping
NP_COMPONENT_DTYPE = {
    5121: numpy.dtype(numpy.uint8),  # GL_UNSIGNED_BYTE
    5123: numpy.dtype(numpy.uint16),  # GL_UNSIGNED_SHORT
    5125: numpy.dtype(numpy.uint32),  # GL_UNSIGNED_INT
    5126: numpy.dtype(numpy.float32),  # GL_FLOAT

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
    supported_extensions = []

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
        self.images = []
        self.samplers = []
        self.textures = []

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
        self.meta.check_extensions(self.supported_extensions)
        self.load_images()
        self.load_samplers()
        self.load_textures()
        self.load_meshes()
        self.load_materials()
        self.load_nodes()

    def load_gltf(self):
        """Loads a gltf json file"""
        with open(self.file) as fd:
            self.meta = GLTFMeta(self.file, json.load(fd))

    def load_glb(self):
        """Loads a binary gltf file"""
        with open(self.file, 'rb') as fd:
            # Check header
            magic = fd.read(4)
            if magic != GLTF_MAGIC_HEADER:
                raise ValueError("{} has incorrect header {} != {}".format(self.file, magic, GLTF_MAGIC_HEADER))

            version = struct.unpack('<I', fd.read(4))[0]
            if version != 2:
                raise ValueError("{} has unsupported version {}".format(self.file, version))

            # Total file size including headers
            _ = struct.unpack('<I', fd.read(4))[0]

            # Chunk 0 - json
            chunk_0_length = struct.unpack('<I', fd.read(4))[0]
            chunk_0_type = fd.read(4)
            if chunk_0_type != b'JSON':
                raise ValueError("Expected JSON chunk, not {} in file {}".format(chunk_0_type, self.file))

            json_meta = fd.read(chunk_0_length).decode()

            # chunk 1 - binary buffer
            chunk_1_length = struct.unpack('<I', fd.read(4))[0]
            chunk_1_type = fd.read(4)
            if chunk_1_type != b'BIN\x00':
                raise ValueError("Expected BIN chunk, not {} in file {}".format(chunk_1_type, self.file))

            self.meta = GLTFMeta(self.file, json.loads(json_meta), binary_buffer=fd.read(chunk_1_length))

    def load_images(self):
        for image in self.meta.images:
            self.images.append(image.load(self.path))

    def load_samplers(self):
        for sampler in self.meta.samplers:
            self.samplers.append(sampler.create())

    def load_textures(self):
        for texture in self.meta.textures:
            mt = MaterialTexture()

            if texture.source is not None:
                mt.texture = self.images[texture.source]

            if texture.sampler is not None:
                mt.sampler = self.samplers[texture.sampler]

            self.textures.append(mt)

    def load_meshes(self):
        for mesh in self.meta.meshes:
            m = mesh.load()
            self.meshes.append(m)
            self.scene.meshes.append(m)

    def load_materials(self):
        # Create material objects
        for mat in self.meta.materials:
            m = Material(mat.name)
            m.color = mat.baseColorFactor
            if mat.baseColorTexture is not None:
                m.mat_texture = self.textures[mat.baseColorTexture['index']]

            self.materials.append(m)
            self.scene.materials.append(m)

        # Map to meshes
        for i, mesh in enumerate(self.meta.meshes):
            if mesh.primitives[0].material is not None:
                self.meshes[i].material = self.materials[mesh.primitives[0].material]

    def load_nodes(self):
        # Start with root nodes in the scene
        for node_id in self.meta.scenes[0].nodes:
            node = self.load_node(self.meta.nodes[node_id])
            self.scene.root_nodes.append(node)

    def load_node(self, meta, parent=None):
        # Create the node
        node = Node()
        self.scene.nodes.append(node)

        if meta.matrix is not None:
            node.matrix = Matrix44(value=meta.matrix)

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
    def __init__(self, file, data, binary_buffer=None):
        """
        :param file: GLTF file name loaded
        :param data: Metadata (json loaded)
        :param binary_buffer: Binary buffer when loading glb files
        """
        self.data = data
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
        self.bufferViews = [GLTFBufferView(i, v) for i, v in enumerate(data['bufferViews'])] \
            if data.get('bufferViews') else []
        self.buffers = [GLTFBuffer(i, b, self.path) for i, b in enumerate(data['buffers'])] \
            if data.get('buffers') else []
        self.accessors = [GLTFAccessor(i, a) for i, a in enumerate(data['accessors'])] \
            if data.get('accessors') else []

        # glb files can contain buffer 0 data
        if binary_buffer:
            self.buffers[0].data = binary_buffer

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

        # Link accessors to mesh primitives
        for mesh in self.meshes:
            for p in mesh.primitives:
                p.indices = self.accessors[p.indices]
                for name, value in p.attributes.items():
                    p.attributes[name] = self.accessors[value]

        # Link buffer views to images
        for image in self.images:
            if image.bufferViewId is not None:
                image.bufferView = self.bufferViews[image.bufferViewId]

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

    def check_extensions(self, supported):
        """
        "extensionsRequired": ["KHR_draco_mesh_compression"],
        "extensionsUsed": ["KHR_draco_mesh_compression"]
        """
        if self.data.get('extensionsRequired'):
            for ext in self.data.get('extensionsRequired'):
                if ext not in supported:
                    raise ValueError("Extension {} not supported".format(ext))

        if self.data.get('extensionsUsed'):
            for ext in self.data.get('extensionsUsed'):
                if ext not in supported:
                    raise ValueError("Extension {} not supported".format(ext))

    def buffers_exist(self):
        """Checks if the bin files referenced exist"""
        for buff in self.buffers:
            if not buff.is_separate_file:
                continue

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
        self.prepare_attrib_mapping()
        component_type, index_vbo = self.load_indices()

        name_map = {
            'POSITION': 'in_position',
            'NORMAL': 'in_normal',
            'TEXCOORD_0': 'in_uv',
            'TANGENT': 'in_tangent',
            'JOINTS_0': 'in_joints',
            'WEIGHTS_0': 'in_heights',
            'COLOR_0': 'in_color0',
        }

        vbos = self.prepare_attrib_mapping()
        vao = VAO(self.name, mode=self.primitives[0].mode or GL.GL_TRIANGLES)
        vao.set_element_buffer(component_type.value, index_vbo)
        attributes = {}

        for vbo_info in vbos:
            vbo = vbo_info.create()
            vao.add_array_buffer(vbo_info.component_type.value, vbo)

            for attr in vbo_info.attributes:
                vao.map_buffer(vbo, name_map[attr[0]], attr[1])
                attributes[attr[0]] = {
                    'name': name_map[attr[0]],
                    'components': attr[1],
                    'type': vbo_info.component_type.value,
                }

        vao.build()
        return Mesh(self.name, vao=vao, attributes=attributes)

    def load_indices(self):
        """Loads the index buffer / polygon list"""
        _, component_type, vbo = self.primitives[0].indices.read(target=GL.GL_ELEMENT_ARRAY_BUFFER)
        return component_type, vbo

    def prepare_attrib_mapping(self):
        buffer_info = []
        """Pre-parse buffer mappings for each VBO to detect interleaved data"""
        for name, accessor in self.primitives[0].attributes.items():
            info = VBOInfo(*accessor.info(target=GL.GL_ARRAY_BUFFER))
            info.attributes.append((name, info.components))

            if buffer_info and buffer_info[-1].buffer_view == info.buffer_view:
                if buffer_info[-1].interleaves(info):
                    buffer_info[-1].merge(info)
                    continue

            buffer_info.append(info)

        return buffer_info

    def get_bbox(self):
        """Get the bounding box for the mesh"""
        accessor = self.primitives[0].attributes.get('POSITION')
        return accessor.min, accessor.max


class VBOInfo:
    """Resolved data about each VBO"""
    def __init__(self, buffer=None, buffer_view=None, target=None,
                 byte_length=None, byte_offset=None,
                 component_type=None, components=None, count=None):
        self.buffer = buffer  # reference to the buffer
        self.buffer_view = buffer_view
        self.target = target
        self.byte_length = byte_length  # Raw byte buffer length
        self.byte_offset = byte_offset  # Raw byte offset
        self.component_type = component_type  # Datatype of each component
        self.components = components
        self.count = count  # number of elements of the component type size
        # list of (name, components) tuples
        self.attributes = []

    def interleaves(self, info):
        """Does the buffer interleave with this one?"""
        return info.byte_offset == self.component_type.size * self.components

    def merge(self, info):
        # NOTE: byte length is the same
        self.components += info.components
        self.attributes += info.attributes

    def create(self):
        """Create the VBO"""
        dtype = NP_COMPONENT_DTYPE[self.component_type.value]
        data = self.buffer.read(byte_length=self.byte_length, byte_offset=self.byte_offset)
        return VBO(numpy.frombuffer(data, count=self.count * self.components, dtype=dtype),
                   target=self.target)

    def __str__(self):
        return "VBOInfo<buffer={}, buffer_view={}, target={}, \n" \
               "        length={}, offset={}, \n" \
               "        component_type={}, components={}, count={}, \n" \
               "        attribs={}".format(self.buffer.id, self.buffer_view.id, self.target,
                                           self.byte_length, self.byte_offset,
                                           self.component_type.value, self.components, self.count,
                                           self.attributes)

    def __repr__(self):
        return str(self)


class GLTFAccessor:
    def __init__(self, accessor_id, data):
        self.id = accessor_id
        self.bufferViewId = data.get('bufferView') or 0
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

    def info(self, target=None):
        """
        Get underlying buffer info for this accessor
        :return: buffer, byte_length, byte_offset, component_type, count
        """
        buffer, target, byte_length, byte_offset = self.bufferView.info(byte_offset=self.byteOffset, target=target)
        return buffer, self.bufferView, target, \
            byte_length, byte_offset, \
            self.componentType, ACCESSOR_TYPE[self.type], self.count


class GLTFBufferView:
    def __init__(self, view_id, data):
        self.id = view_id
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

    def read_raw(self):
        return self.buffer.read(byte_length=self.byteLength, byte_offset=self.byteOffset)

    def info(self, byte_offset=0, target=None):
        """
        Get the underlying buffer info
        :param byte_offset: byte offset from accessor
        :param target: buffer target (elements or data array)
        :return: buffer, target, byte_length, byte_offset
        """
        return self.buffer, BUFFER_TARGETS[target], self.byteLength, byte_offset + self.byteOffset


class GLTFBuffer:
    def __init__(self, buffer_id, data, path):
        self.id = buffer_id
        self.path = path
        self.byteLength = data.get('byteLength')
        self.uri = data.get('uri')
        self.data = None

    @property
    def has_data_uri(self):
        """Is data embedded in json?"""
        if not self.uri:
            return False

        return self.uri.startswith("data:")

    @property
    def is_separate_file(self):
        """Buffer represents an independent bin file?"""
        return self.uri is not None and not self.has_data_uri

    def open(self):
        if self.data:
            return

        if self.has_data_uri:
            self.data = base64.b64decode(self.uri[self.uri.find(',') + 1:])
            return

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

        if self.matrix is None:
            self.matrix = matrix44.create_identity()
        if self.translation is not None:
            self.matrix = matrix44.create_from_translation(self.translation)
        if self.rotation is not None:
            q = quaternion.create(self.rotation[0], self.rotation[1], self.rotation[2], self.rotation[3])
            m = matrix44.create_from_quaternion(q)
            self.matrix = matrix44.multiply(m, self.matrix)
        if self.scale is not None:
            self.matrix = matrix44.multiply(matrix44.create_from_scale(self.scale), self.matrix)

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

        pbr = data['pbrMetallicRoughness']
        self.baseColorFactor = pbr.get('baseColorFactor')
        self.baseColorTexture = pbr.get('baseColorTexture')
        self.metallicFactor = pbr.get('metallicFactor')
        self.emissiveFactor = data.get('emissiveFactor')


class GLTFImage:
    """
    Represent texture data.
    May be a file, embedded data or pointer to data in bufferview
    """
    def __init__(self, data):
        self.uri = data.get('uri')
        self.bufferViewId = data.get('bufferView')
        self.bufferView = None
        self.mimeType = data.get('mimeType')

    def load(self, path):
        # data:image/png;base64,iVBOR

        texture = Texture(self.uri, mipmap=True, anisotropy=8)

        # Image is stored in bufferView
        if self.bufferView is not None:
            image = Image.open(io.BytesIO(self.bufferView.read_raw()))
        # Image is embedded
        elif self.uri and self.uri.startswith('data:'):
            data = self.uri[self.uri.find(',') + 1:]
            image = Image.open(io.BytesIO(base64.b64decode(data)))
        else:
            path = os.path.join(path, self.uri)
            image = Image.open(path)

        texture.set_image(image, flip=False)
        return texture


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

    def create(self):
        return samplers.create_sampler(
            mipmap=True,
            mag_filter=self.magFilter,
            min_filter=self.minFilter,
            anisotropy=8,
            wrap_s=self.wrapS,
            wrap_t=self.wrapT,
        )


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
