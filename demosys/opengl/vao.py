import moderngl as mgl
from OpenGL import GL

from demosys.opengl import types
from demosys.opengl import ShaderProgram
from demosys import context

DRAW_MODES = {
    mgl.TRIANGLES: 'TRIANGLES',
    mgl.TRIANGLE_FAN: 'TRIANGLE_FAN',
    mgl.TRIANGLE_STRIP: 'TRIANGLE_STRIP',
    mgl.TRIANGLES_ADJACENCY: 'TRIANGLES_ADJACENCY',
    mgl.TRIANGLE_STRIP_ADJACENCY: 'TRIANGLE_STRIP_ADJACENCY',
    mgl.POINTS: 'POINTS',
    mgl.LINES: 'LINES',
    mgl.LINE_STRIP: 'LINE_STRIP',
    mgl.LINE_LOOP: 'LINE_LOOP',
    mgl.LINES_ADJACENCY: 'LINES_ADJACENCY',
}


class VAOError(Exception):
    pass


class ArrayBuffer:
    """Container for a vbo with additional information"""
    def __init__(self, buffer_format: str, vbo: mgl.Buffer):
        """
        :param format: The format of the buffer
        :param vbo: The vbo object
        """
        self.buffer_format = types.buffer_format(buffer_format)
        self.vbo = vbo
        self.array_maps = []

        # Calculated during VAO creation
        self.stride = 0
        self.vertex_format = []

        # Sanity check byte size
        if self.size % self.element_size != 0:
            raise VAOError("Buffer with type {} has size not aligning with {}. Remainder: ".format(
                self.buffer_format, self.element_size, self.size % self.element_size,
            ))

        self.elements = self.size // self.element_size

    @property
    def element_size(self):
        return self.buffer_format.bytes_per_component

    @property
    def size(self):
        """
        :return: Size of the vbo in bytes
        """
        return self.vbo.size

    @property
    def vertices(self):
        """
        :return: The number of vertices based on the current stride
        """
        if self.size % self.stride != 0:
            raise VAOError("size % stride != 0")
        return self.size // self.stride


class ArrayMapping:
    """Keeps track of vbo to attribute mapping"""
    def __init__(self, array_buffer, attrib_name, components, byte_offset):
        """
        :param array_buffer: The array buffer
        :param attrib_name: Name of the attribute
        :param components: Number of components
        :param offset: Byte offset in the buffer
        """
        array_buffer.array_maps.append(self)
        self.array_buffer = array_buffer
        self.attrib_name = attrib_name
        self.components = components
        self.byte_offset = byte_offset


class VAO:
    """Vertex Array Object"""
    def __init__(self, name, mode=mgl.TRIANGLES):
        """
        Create and empty VAO

        :param name: The name for debug purposes
        :param mode: Default draw mode for this VAO
        """
        self.name = name
        self.mode = mode

        try:
            DRAW_MODES[self.mode]
        except KeyError:
            raise VAOError("Invalid draw mode. Options are {}".format(DRAW_MODES.values()))

        self.array_buffer_map = {}

        self.array_mapping = []
        self.array_mapping_map = {}

        self.element_buffer = None
        self.vertex_count = 0
        self.vaos = {}

    def draw(self, shader, mode=None):
        """
        Draw the VAO.
        Will use ``glDrawElements`` if an element buffer is present
        and ``glDrawArrays`` if no element array is present.

        :param mode: Override the draw mode (GL_TRIANGLES etc)
        """
        vao = self.generate_vao_combo(shader)

        # if self.element_buffer:
        #     if mode is not None:
        #         GL.glDrawElements(mode,
        #                           self.element_buffer.elements,
        #                           self.element_buffer.format,
        #                           self.element_buffer.vbo)
        #     else:
        #         GL.glDrawElements(self.mode or GL.GL_TRIANGLES,
        #                           self.element_buffer.elements,
        #                           self.element_buffer.format,
        #                           self.element_buffer.vbo)
        # else:
        #     if mode is not None:
        #         GL.glDrawArrays(mode, 0, self.vertex_count)
        #     else:
        #         GL.glDrawArrays(self.mode, 0, self.vertex_count)

    def add_buffer(self, format: str, buffer: mgl.Buffer):
        """
        Register a buffer/vbo for the VAO. This can be called multiple times.
        adding multiple buffers (interleaved or not)

        :param format: The format of the buffer ('f', 'u', 'i')
        :param buffer: The buffer object
        """
        if not isinstance(buffer, mgl.Buffer):
            raise VAOError("buffer parameter must be a moderngl.Buffer instance")

        self.array_buffer_map[buffer.glo] = ArrayBuffer(format, buffer)

    def set_element_buffer(self, buffer_format: str, buffer: mgl.Buffer):
        """
        Set the index buffer for this VAO

        :param buffer_format: The format of the element buffer ('u', 'u1', 'u2', 'u4' etc)
        :param buffer: the vbo object
        """
        if not isinstance(buffer, mgl.Buffer):
            raise VAOError("buffer parameter must be a moderngl.Buffer instance")

        self.element_buffer = ArrayBuffer(buffer_format, buffer)

    def map_buffer(self, buffer: mgl.Buffer, attrib_name: str, components: int):
        """
        Map parts of the vbos to an attribute name.
        This can be called multiple times to describe hos the buffers map to attribute names.
        If the same vbo is passed more than once it must be an interleaved buffer.

        :param buffer: The vbo/buffer
        :param attrib_name: Name of the attribute in the shader
        :param components: Number of components (for example 3 for a x, y, x position)
        """
        if not isinstance(buffer, mgl.Buffer):
            raise VAOError("buffer parameter must be an mgl.Buffer instance")

        ab = self.array_buffer_map.get(buffer.glo)
        if not ab:
            raise VAOError("buffer {} not unknown. "
                           "Forgot to call add_buffer(..)?".format(buffer.glo))

        # FIXME: Determine byte size based on data type in VBO
        byte_offset = ab.stride
        ab.stride += components * ab.element_size
        am = ArrayMapping(ab, attrib_name, components, byte_offset)

        self.array_mapping.append(am)
        self.array_mapping_map[attrib_name] = am

    def build(self):
        """
        Finalize the VAO.
        This runs various sanity checks on the input data.
        """
        if len(self.array_buffer_map) == 0:
            raise VAOError("VAO has no buffers")

        for key, buff in self.array_buffer_map.items():
            if buff.stride == 0:
                raise VAOError("Buffers {} was never mapped to attributes in VAO {}".format(key, self.name))

        # Check that all buffers have the same number of units
        last_vertices = -1
        for name, buf in self.array_buffer_map.items():
            vertices = buf.vertices
            if last_vertices > -1:
                if last_vertices != vertices:
                    raise VAOError("{} num_vertices {} != {}".format(name, last_vertices, vertices))

        self.vertex_count = vertices
        print("VAO {} has {} vertices".format(self.name, self.vertex_count))

    def generate_vao_combo(self, shader):
        """
        Create a VAO based on the shader's attribute specification.
        This is called by ``bind(shader)`` and should not be messed with
        unless you are absolutely sure about what you are doing.

        :param shader: The shader we are generating the combo for
        :return: A new VAOCombo object with the correct attribute binding
        """
        # Return the combo if already generated
        vao = self.vaos.get(shader.vao_key)
        if vao:
            return vao

        print("Generating VAO Combo for {} using key {}".format(self.name, shader.vao_key))

        array_mapping_list = []
        # Build the vao according to the shader's attribute specifications
        for attribute in shader.attribute_list:
            # Do we actually have an array mapping with this attribute name?
            mapping = self.array_mapping_map.get(attribute.name)
            if not mapping:
                raise VAOError("VAO {} don't know about the attribute '{}'".format(self.name, attribute.name))

            array_mapping_list.append(mapping)

        # Do the data binding for this VAO: Order is the same as the attribList
        for i, mapping in enumerate(array_mapping_list):
            print(" - > [{name}] loc {loc} components={comp} format={frmt} stride={stride} offset={offset}".format(
                name=shader.attribute_list[i].name,
                loc=shader.attribute_list[i].location,
                comp=mapping.components,
                frmt=mapping.array_buffer.buffer_format,
                stride=mapping.array_buffer.stride,
                offset=mapping.byte_offset,
            ))

            format = types.attribute_format("{}{}".format(
                mapping.components,
                mapping.array_buffer.buffer_format.format
            ))
            mapping.array_buffer.vertex_format.append(format)

        vao = "Dummy"
        # if self.element_buffer:
        #     self.element_buffer.vbo.bind()
        # else:
        #     context.ctx().vertex_array()

        self.vaos[shader.vao_key] = vao

        return vao
