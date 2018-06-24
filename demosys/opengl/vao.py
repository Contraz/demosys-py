import numpy
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
    def __init__(self, buffer: mgl.Buffer, buffer_format: str, attributes=None):
        """
        :param buffer: The vbo object
        :param format: The format of the buffer
        """
        self.buffer = buffer
        self.attrib_formats = types.parse_attribute_formats(buffer_format)
        self.attributes = attributes

        # Sanity check byte size
        if self.buffer.size % self.vertex_size != 0:
            raise VAOError("Buffer with type {} has size not aligning with {}. Remainder: ".format(
                buffer_format, self.vertex_size, self.buffer.size % self.vertex_size,
            ))

        self.vertices = self.buffer.size // self.vertex_size

    @property
    def vertex_size(self) -> int:
        return sum(f.bytes_total for f in self.attrib_formats)

    def content(self, attributes: List[str]):
        """Build content tuple for the buffer"""
        formats = []
        attrs = []
        for attrib_format, attrib in zip(self.attrib_formats, self.attributes):
            if attrib not in attributes:
                formats.append(attrib_format.pad_str())
                continue

            formats.append(attrib_format.format)
            attrs.append(attrib)

            attributes.remove(attrib)

        if len(attrs) == 0:
            return None

        return (
            self.buffer,
            " ".join(formats),
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
        self._index_buffer = None
        self._index_buffer_format = None

        self.vertex_count = 0
        self.vaos = {}

    def draw(self, shader: ShaderProgram, mode=None):
        """
        Draw the VAO.
        Will use ``glDrawElements`` if an element buffer is present
        and ``glDrawArrays`` if no element array is present.

        :param shader: The shader to draw with
        :param mode: Override the draw mode (GL_TRIANGLES etc)
        """
        vao = self._create_vao_instance(shader)

        if mode is None:
            mode = self.mode

        vao.render(mode)

    def transform(self, shader, buffer: mgl.Buffer, mode=None, vertices=-1, first=0, instances=1):
        """
        Transform vertices. Stores the output in a single buffer.

        :param buffer: The buffer to store the output
        :param mode: Draw mode (for example `POINTS`
        :param vertices: The number of vertices to transform
        :param first: The index of the first vertex to start with
        :param instances: The number of instances
        :return:
        """
        vao = self._create_vao_instance(shader)

        if mode is None:
            mode = self.mode

        vao.transform(buffer, mode=mode, vertices=vertices, first=first, instances=instances)

    def buffer(self, buffer, buffer_format: str, attribute_names):
        """
        Register a buffer/vbo for the VAO. This can be called multiple times.
        adding multiple buffers (interleaved or not)

        :param buffer: The buffer object. Can be ndarray or Buffer
        :param buffer_format: The format of the buffer ('f', 'u', 'i')
        """
        if not isinstance(buffer, mgl.Buffer) and not isinstance(buffer, numpy.ndarray):
            raise VAOError("buffer parameter must be a moderngl.Buffer or numpy.ndarray instance")

        if isinstance(buffer, numpy.ndarray):
            buffer = context.ctx().buffer(buffer.tobytes())

        formats = buffer_format.split()
        if len(formats) != len(attribute_names):
            raise VAOError("Format '{}' does not describe attributes {}".format(buffer_format, attribute_names))

        self.buffers.append(BufferInfo(buffer, buffer_format, attribute_names))
        self.vertex_count = self.buffers[-1].vertices

    def index_buffer(self, buffer_format: str, buffer):
        """
        Set the index buffer for this VAO

        :param buffer_format: The format of the element buffer ('u', 'u1', 'u2', 'u4' etc)
        :param buffer: Buffer object or ndarray
        """
        if not isinstance(buffer, mgl.Buffer) and not isinstance(buffer, numpy.ndarray):
            raise VAOError("buffer parameter must be a moderngl.Buffer or numpy.ndarray instance")

        if isinstance(buffer, numpy.ndarray):
            buffer = context.ctx().buffer(buffer.tobytes())

        self._index_buffer = buffer
        self._index_buffer_format = buffer_format

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

        if self._index_buffer:
            vao = context.ctx().vertex_array(shader.program, vao_content, self._index_buffer)
        else:
            vao = context.ctx().vertex_array(shader.program, vao_content)
        self.vaos[shader.vao_key] = vao

        return vao
