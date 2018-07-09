import os

import moderngl as mgl
from demosys import context
from demosys.conf import settings

VERTEX_SHADER = 'VERTEX_SHADER'
GEOMETRY_SHADER = 'GEOMETRY_SHADER'
FRAGMENT_SHADER = 'FRAGMENT_SHADER'


class ShaderProgram:
    """
    Represents a shader program
    """
    def __init__(self, path=None, name=None):
        """
        Create a shader using either a file path or a name
        :param path: Full file path to the shader
        :param name: Name of the shader (debug purposes)
        """
        self.ctx = context.ctx()
        if not path and not name:
            raise ShaderError("Shader must have a path or a name")

        self.path = path

        if not name:
            self.name = os.path.basename(path)
        else:
            self.name = name

        self._vertex_source = None
        self._fragment_source = None
        self._geometry_source = None

        self.program = None
        # Shader inputs
        self.uniform_map = {}

        self.attribute_list = []
        self.attribute_map = {}

        # A string of concatenated attribute names
        self.attribute_key = None
        # Unique key for VAO instances containing shader id and attributes
        self.vao_key = None

    @property
    def mglo(self):
        """The ModernGL Program object"""
        return self.program

    def uniform(self, name, value=None):
        """
        Set or get a uniform.
        If no `value` is specificed, the unform will be returned

        :param name: Name of the uniform
        :param value: Value for the uniform
        :return: (optional) Uniform objects
        """
        uniform = self.uniform_map.get(name)
        if not uniform:
            msg = "Uniform '{}' not found in shader {}".format(name, self.name)
            if settings.SHADER_STRICT_VALIDATION:
                raise ShaderError(msg)
            else:
                print(msg)
            return None

        if value is None:
            return uniform

        if isinstance(value, bytes):
            uniform.write(value)
        else:
            uniform.value = value

    def set_source(self, source: str):
        """
        Set a single source file.
        This is used when you have all shaders in one file separated by preprocessors.

        :param source: (string) The shader source
        """
        self.set_vertex_source(source)

        if GEOMETRY_SHADER in source:
            self.set_geometry_source(source)

        if FRAGMENT_SHADER in source:
            self.set_fragment_source(source)

    def set_vertex_source(self, source: str):
        """
        Set the vertex shader source

        :param source: (string) Vertex shader source
        """
        self._vertex_source = ShaderSource(VERTEX_SHADER, self.name, source)

    def set_fragment_source(self, source: str):
        """
        Set the fragment shader source

        :param source: (string) Fragment shader source
        """
        self._fragment_source = ShaderSource(FRAGMENT_SHADER, self.name, source)

    def set_geometry_source(self, source: str):
        """
        Set the geometry shader source

        :param source: (string) Geometry shader source
        """
        self._geometry_source = ShaderSource(GEOMETRY_SHADER, self.name, source)

    def prepare(self, reload=False):
        """
        Compiles all the shaders and links the program.
        If the linking is successful it builds the uniform and attribute map.

        :param reload: (boolean) Are we reloading this shader?
        """
        params = {'vertex_shader': self._vertex_source.source}

        if self._geometry_source:
            params.update({'geometry_shader': self._geometry_source.source})

        if self._fragment_source:
            params.update({'fragment_shader': self._fragment_source.source})

        # If no fragment shader is present we are doing transform feedback
        if not self._fragment_source:
            # Out attributes is present in geometry shader if present
            if self._geometry_source:
                out_attribs = self._geometry_source.find_out_attribs()
            # Otherwise they are specified in vertex shader
            else:
                out_attribs = self._vertex_source.find_out_attribs()

            print("Out attributes for transform feedback", out_attribs)
            params.update({'varyings': out_attribs})

        # Raises mgl.Error
        program = self.ctx.program(**params)

        if reload:
            self.program.release()

        self.program = program

        # Build internal lookups
        self._build_uniform_map()
        self._build_attribute_map()

    def _delete(self):
        """Frees the memory and invalidates the name associated with the program"""
        if self.program:
            self.program.release()

    def _build_uniform_map(self):
        """
        Builds an internal uniform map by querying the program.
        This way we don't have to query OpenGL (can cause slowdowns)
        """
        self.uniform_map = {k: v for k, v in self.program._members.items() if isinstance(v, mgl.Uniform)}
        print("ShaderProgram {} has {} uniform(s)".format(self.name, len(self.uniform_map)))

        for name, uniform in self.uniform_map.items():
            print(" - Uniform[{}] {} {} {}".format(
                uniform.location, uniform.name, uniform.dimension, uniform.array_length
            ))

    def _build_attribute_map(self):
        """
        Builds an internal attribute map by querying the program.
        This way we don't have to query OpenGL (can cause slowdowns)
        This information is also used when the shader and VAO negotiates the buffer binding.
        """
        # Reset attribute storage to support reloading
        self.attribute_list = []
        self.attribute_map = {}

        for name, attribute in self.program._members.items():
            if not isinstance(attribute, mgl.Attribute):
                continue

            self.attribute_list.append(attribute)
            self.attribute_map[name] = attribute

            print(" - Attribute[{}] {} {} ({})".format(
                attribute.location, attribute.name, attribute.array_length, attribute.dimension
            ))

        self.attribute_key = ','.join(name for name in sorted(self.attribute_map.keys()))
        print("Shader attribute key:", self.attribute_key)

        self.vao_key = "{}:{}".format(self.program.glo, self.attribute_key)
        print("Shader VAO key:", self.vao_key)


class ShaderError(Exception):
    pass


class ShaderSource:
    """
    Helper class to deal with shader source files.
    This represents a single shader (vert/frag/geo)
    """
    def __init__(self, shader_type, name, source):
        self.type = shader_type
        self.name = name
        self.source = source
        self.lines = None
        self.shader = None

        if not isinstance(self.source, str):
            raise ShaderError("Shader source is not a string: {source}")

        self.lines = self.source.split('\n')

        # Make sure version is present
        if not self.lines[0].startswith("#version"):
            self.print()
            raise ShaderError(
                "Missing #version in shader {}. A version must be defined in the first line".format(self.name),
            )

        # Add preprocessors to source
        if self.type == VERTEX_SHADER:
            self.lines.insert(1, "#define VERTEX_SHADER 1")
        elif self.type == FRAGMENT_SHADER:
            self.lines.insert(1, "#define FRAGMENT_SHADER 1")
        elif self.type == GEOMETRY_SHADER:
            self.lines.insert(1, "#define GEOMETRY_SHADER 1")

        self.source = '\n'.join(self.lines)

    def find_out_attribs(self):
        """
        Get all out attributes in the shader source.
        :return: List of attribute names
        """
        names = []
        for line in self.lines:
            if line.strip().startswith("out "):
                names.append(line.split()[2].replace(';', ''))
        return names

    def print(self):
        """Print the shader lines"""
        print("---[ START {} ]---".format(self.name))

        for i, line in enumerate(self.lines):
            print("{}: {}".format(str(i).zfill(3), line))

        print("---[ END {} ]---".format(self.name))
