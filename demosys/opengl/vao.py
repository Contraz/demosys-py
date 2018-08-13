from typing import List

import numpy

import moderngl
from demosys import context
from demosys.opengl import types

# For sanity checking draw modes when creating the VAO
DRAW_MODES = {
    moderngl.TRIANGLES: 'TRIANGLES',
    moderngl.TRIANGLE_FAN: 'TRIANGLE_FAN',
    moderngl.TRIANGLE_STRIP: 'TRIANGLE_STRIP',
    moderngl.TRIANGLES_ADJACENCY: 'TRIANGLES_ADJACENCY',
    moderngl.TRIANGLE_STRIP_ADJACENCY: 'TRIANGLE_STRIP_ADJACENCY',
    moderngl.POINTS: 'POINTS',
    moderngl.LINES: 'LINES',
    moderngl.LINE_STRIP: 'LINE_STRIP',
    moderngl.LINE_LOOP: 'LINE_LOOP',
    moderngl.LINES_ADJACENCY: 'LINES_ADJACENCY',
}


class BufferInfo:
    """Container for a vbo with additional information"""
    def __init__(self, buffer: moderngl.Buffer, buffer_format: str, attributes=None, per_instance=False):
        """
        :param buffer: The vbo object
        :param format: The format of the buffer
        """
        self.buffer = buffer
        self.attrib_formats = types.parse_attribute_formats(buffer_format)
        self.attributes = attributes
        self.per_instance = per_instance

        # Sanity check byte size
        if self.buffer.size % self.vertex_size != 0:
            raise VAOError("Buffer with type {} has size not aligning with {}. Remainder: {}".format(
                buffer_format, self.vertex_size, self.buffer.size % self.vertex_size
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

        if not attrs:
            return None

        return (
            self.buffer,
            "{}{}".format(" ".join(formats), '/i' if self.per_instance else ''),
            *attrs
        )

    def has_attribute(self, name):
        return name in self.attributes


class VAO:
    """
    Represents a vertex array object.
    A name must be provided for debug puporses.
    The default draw mode is ``moderngl.TRIANGLES``
    """
    def __init__(self, name, mode=moderngl.TRIANGLES):
        """
        Create and empty VAO

        :param name: The name for debug purposes
        :param mode: Default draw mode for this VAO
        """
        self.ctx = context.ctx()
        self.name = name
        self.mode = mode

        try:
            DRAW_MODES[self.mode]
        except KeyError:
            raise VAOError("Invalid draw mode. Options are {}".format(DRAW_MODES.values()))

        self.buffers = []
        self._index_buffer = None
        self._index_element_size = None

        self.vertex_count = 0
        self.vaos = {}

    def render(self, program: moderngl.Program, mode=None, vertices=-1, first=0, instances=1):
        """
        Render the VAO.

        :param program: The program to draw with
        :param mode: Override the draw mode (TRIANGLES etc)
        :param vertices: The number of vertices to transform
        :param first: The index of the first vertex to start with
        :param instances: The number of instances
        """
        vao = self.instance(program)

        if mode is None:
            mode = self.mode

        vao.render(mode, vertices=vertices, first=first, instances=instances)

    def render_indirect(self, program: moderngl.Program, buffer, mode=None, count=-1, *, first=0):
        """
        The render primitive (mode) must be the same as the input primitive of the GeometryShader.
        The draw commands are 5 integers: (count, instanceCount, firstIndex, baseVertex, baseInstance).

        :param program: (Buffer) Indirect drawing commands.
        :param buffer: (Buffer) Indirect drawing commands.
        :param mode:  (int) By default :py:data:`TRIANGLES` will be used.
        :param count: (int) The number of draws.
        :param first: (int) The index of the first indirect draw command.
        """
        vao = self.instance(program)

        if mode is None:
            mode = self.mode

        vao.render_indirect(buffer, mode=mode, count=count, first=first)

    def transform(self, program: moderngl.Program, buffer: moderngl.Buffer,
                  mode=None, vertices=-1, first=0, instances=1):
        """
        Transform vertices. Stores the output in a single buffer.

        :param program: The program
        :param buffer: The buffer to store the output
        :param mode: Draw mode (for example `POINTS`
        :param vertices: The number of vertices to transform
        :param first: The index of the first vertex to start with
        :param instances: The number of instances
        """
        vao = self.instance(program)

        if mode is None:
            mode = self.mode

        vao.transform(buffer, mode=mode, vertices=vertices, first=first, instances=instances)

    def buffer(self, buffer, buffer_format: str, attribute_names, per_instance=False):
        """
        Register a buffer/vbo for the VAO. This can be called multiple times.
        adding multiple buffers (interleaved or not)

        :param buffer: The buffer object. Can be ndarray or Buffer
        :param buffer_format: The format of the buffer ('f', 'u', 'i')
        :returns: The buffer object
        """
        if not isinstance(attribute_names, list):
            attribute_names = [attribute_names, ]

        if not type(buffer) in [moderngl.Buffer, numpy.ndarray, bytes]:
            raise VAOError("buffer parameter must be a moderngl.Buffer, numpy.ndarray or bytes instance")

        if isinstance(buffer, numpy.ndarray):
            buffer = self.ctx.buffer(buffer.tobytes())

        if isinstance(buffer, bytes):
            buffer = self.ctx.buffer(data=buffer)

        formats = buffer_format.split()
        if len(formats) != len(attribute_names):
            raise VAOError("Format '{}' does not describe attributes {}".format(buffer_format, attribute_names))

        self.buffers.append(BufferInfo(buffer, buffer_format, attribute_names, per_instance=per_instance))
        self.vertex_count = self.buffers[-1].vertices

        return buffer

    def index_buffer(self, buffer, index_element_size=4):
        """
        Set the index buffer for this VAO

        :param buffer: Buffer object or ndarray
        :param index_element_size: Byte size of each element. 1, 2 or 4
        """
        if not type(buffer) in [moderngl.Buffer, numpy.ndarray, bytes]:
            raise VAOError("buffer parameter must be a moderngl.Buffer, numpy.ndarray or bytes instance")

        if isinstance(buffer, numpy.ndarray):
            buffer = self.ctx.buffer(buffer.tobytes())

        if isinstance(buffer, bytes):
            buffer = self.ctx.buffer(data=buffer)

        self._index_buffer = buffer
        self._index_element_size = index_element_size

    def instance(self, program: moderngl.Program) -> moderngl.VertexArray:
        """
        Obtain the moderngl.VertexArray instance for the program

        :return: moderngl.VertexArray
        """
        vao = self.vaos.get(program.glo)
        if vao:
            return vao

        program_attributes = [name for name, attr in program._members.items() if isinstance(attr, moderngl.Attribute)]

        # Make sure all attributes are covered
        for attrib_name in program_attributes:
            # Ignore built in attributes for now
            if attrib_name.startswith('gl_'):
                continue

            # Do we have a buffer mapping to this attribute?
            if not sum(buffer.has_attribute(attrib_name) for buffer in self.buffers):
                raise VAOError("VAO {} doesn't have attribute {} for program {}".format(
                    self.name, attrib_name, program.name))

        vao_content = []

        # Pick out the attributes we can actually map
        for buffer in self.buffers:
            content = buffer.content(program_attributes)
            if content:
                vao_content.append(content)

        # Any attribute left is not accounted for
        if program_attributes:
            for attrib_name in program_attributes:
                if attrib_name.startswith('gl_'):
                    continue

                raise VAOError("Did not find a buffer mapping for {}".format([n for n in program_attributes]))

        # Create the vao
        if self._index_buffer:
            vao = context.ctx().vertex_array(program, vao_content,
                                             self._index_buffer, self._index_element_size)
        else:
            vao = context.ctx().vertex_array(program, vao_content)

        self.vaos[program.glo] = vao
        return vao

    def release(self, buffer=True):
        """
        Destroy the vao object

        :param buffers: (bool) also release buffers
        """
        for key, vao in self.vaos:
            vao.release()

        if buffer:
            for buff in self.buffers:
                buff.buffer.release()

            if self._index_buffer:
                self._index_buffer.release()


class VAOError(Exception):
    pass
