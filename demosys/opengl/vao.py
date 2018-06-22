from typing import List
import moderngl as mgl

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


class BufferInfo:
    """Container for a vbo with additional information"""
    def __init__(self, buffer: mgl.Buffer, buffer_format: str, attributes):
        """
        :param buffer: The vbo object
        :param format: The format of the buffer
        """
        self.buffer = buffer
        self.attrib_formats = types.parse_attribute_formats(buffer_format)
        self.attributes = attributes

        # Sanity check byte size
        if self.buffer.size % self.element_size != 0:
            raise VAOError("Buffer with type {} has size not aligning with {}. Remainder: ".format(
                buffer_format, self.element_size, self.buffer.size % self.element_size,
            ))

        self.elements = self.buffer.size // self.element_size

    @property
    def element_size(self) -> int:
        return sum(f.bytes_per_component for f in self.attrib_formats)

    @property
    def vertices(self) -> int:
        """
        :return: The number of vertices based on the current stride
        """
        return self.buffer.size // self.element_size

    def content(self, attributes: List[str]):
        """Build content tuple for the buffer"""
        formats = []
        attrs = []
        for i, attrib in enumerate(self.attributes):
            if attrib not in attributes:
                continue

            formats.append(self.attrib_formats[i])
            attrs.append(attrib)
            attributes.remove(attrib)

        if len(attrs) == 0:
            return None

        return (
            self.buffer,
            *(f.format for f in formats),
            *attrs
        )

    def has_attribute(self, name):
        return name in self.attributes


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

        self.buffers = []
        self.element_buffer = None

        self.vertex_count = 0
        self.vaos = {}

    def draw(self, shader: ShaderProgram, mode=None):
        """
        Draw the VAO.
        Will use ``glDrawElements`` if an element buffer is present
        and ``glDrawArrays`` if no element array is present.

        :param mode: Override the draw mode (GL_TRIANGLES etc)
        """
        vao = self._create_vao_instance(shader)

        mode = self.mode or mgl.TRIANGLES
        vao.render(mode)

    def buffer(self, buffer: mgl.Buffer, buffer_format: str, attribute_names):
        """
        Register a buffer/vbo for the VAO. This can be called multiple times.
        adding multiple buffers (interleaved or not)

        :param buffer: The buffer object
        :param buffer_format: The format of the buffer ('f', 'u', 'i')
        """
        if not isinstance(buffer, mgl.Buffer):
            raise VAOError("buffer parameter must be a moderngl.Buffer instance")

        formats = buffer_format.split()
        if len(formats) != len(attribute_names):
            raise VAOError("Format '{}' does not describe attributes {}".format(buffer_format, attribute_names))

        self.buffers.append(BufferInfo(buffer, buffer_format, attribute_names))
        self.vertex_count = self.buffers[-1].vertices

    def element_buffer(self, buffer_format: str, buffer: mgl.Buffer):
        """
        Set the index buffer for this VAO

        :param buffer_format: The format of the element buffer ('u', 'u1', 'u2', 'u4' etc)
        :param buffer: the vbo object
        """
        if not isinstance(buffer, mgl.Buffer):
            raise VAOError("buffer parameter must be a moderngl.Buffer instance")

        self.element_buffer = BufferInfo(buffer, buffer_format)

    def _create_vao_instance(self, shader):
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

        # Make sure all attributes are covered
        for attrib in shader.attribute_list:
            if not sum(b.has_attribute(attrib.name) for b in self.buffers):
                raise VAOError("VAO {} doesn't have attribute {} for program {}".format(
                    self.name, attrib.name, shader.name))

        attributes = [a.name for a in shader.attribute_list]
        vao_content = []

        for buffer in self.buffers:
            content = buffer.content(attributes)
            if content:
                vao_content.append(content)

        if len(attributes) > 0:
            raise VAOError("Did not find a buffer mapping for {}".format([n.name for n in attributes]))

        vao = context.ctx().vertex_array(shader.program, vao_content)
        self.vaos[shader.vao_key] = vao

        return vao
