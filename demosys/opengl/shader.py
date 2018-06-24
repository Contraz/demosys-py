import moderngl
import os

from OpenGL import GL

from demosys import context
from demosys.conf import settings


class ShaderError(Exception):
    pass


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
        if not path and not name:
            raise ShaderError("Shader must have a path or a name")

        self.path = path

        if not name:
            self.name = os.path.basename(path)
        else:
            self.name = name

        self.vertex_source = None
        self.frag_source = None
        self.geo_source = None

        self.program = None
        # Shader inputs
        self.uniform_map = {}

        self.attribute_list = []
        self.attribute_map = {}

        # A string of concatenated attribute names
        self.attribute_key = None
        # Unique key for VAO instances containing shader id and attributes
        self.vao_key = None

    def uniform(self, name, value=None):
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

    def bind(self):
        """
        Bind the shader. Ideally we should never need to use this as programs are bound to VAOs directly
        """
        GL.glUseProgram(self.program.glo)

    def set_source(self, source):
        """
        Set a single source file.
        This is used when you have all shaders in one file separated by preprocessors.

        :param source: (string) The shader source
        """
        self.set_vertex_source(source)

        if 'GEOMETRY_SHADER' in source:
            self.set_geometry_source(source)

        if 'FRAGMENT_SHADER' in source:
            self.set_fragment_source(source)

    def set_vertex_source(self, source):
        """
        Set the vertex shader source

        :param source: (string) Vertex shader source
        """
        self.vertex_source = ShaderSource(GL.GL_VERTEX_SHADER, self.name, source)

    def set_fragment_source(self, source):
        """
        Set the fragment shader source

        :param source: (string) Fragment shader source
        """
        self.frag_source = ShaderSource(GL.GL_FRAGMENT_SHADER, self.name, source)

    def set_geometry_source(self, source):
        """
        Set the geometry shader source

        :param source: (string) Geometry shader source
        """
        self.geo_source = ShaderSource(GL.GL_GEOMETRY_SHADER, self.name, source)

    def prepare(self):
        """
        Compiles all the shaders and links the program.
        If the linking is successful, it builds the uniform and attribute map.
        """
        params = {'vertex_shader': self.vertex_source.source}

        if self.geo_source:
            params.update({'geometry_shader': self.geo_source.source})

        if self.frag_source:
            params.update({'fragment_shader': self.frag_source.source})

        # If no fragment shader is present we are doing transform feedback
        if not self.frag_source:
            # Out attributes is present in geometry shader if present
            if self.geo_source:
                out_attribs = self.geo_source.find_out_attribs()
            # Otherwise they are specified in vertex shader
            else:
                out_attribs = self.vertex_source.find_out_attribs()

            print("Out attributes for transform feedback", out_attribs)
            params.update({'varyings': out_attribs})

        # Raises mgl.Error
        self.program = context.ctx().program(**params)

        # Build internal lookups
        self.build_uniform_map()
        self.build_attribute_map()

    def _delete(self):
        """Frees the memory and invalidates the name associated with the program"""
        if self.program:
            self.program.release()

    def build_uniform_map(self):
        """
        Builds an internal uniform map by querying the program.
        This way we don't have to query OpenGL (can cause slowdowns)
        """
        self.uniform_map = {k: v for k, v in self.program._members.items() if isinstance(v, moderngl.Uniform)}
        print("ShaderProgram {} has {} uniform(s)".format(self.name, len(self.uniform_map)))

        for name, uniform in self.uniform_map.items():
            print(" - Uniform[{}] {} {} {}".format(
                uniform.location, uniform.name, uniform.dimension, uniform.array_length
            ))

    def build_attribute_map(self):
        """
        Builds an internal attribute map by querying the program.
        This way we don't have to query OpenGL (can cause slowdowns)
        This information is also used when the shader and VAO negotiates the buffer binding.
        """
        for name, attribute in self.program._members.items():
            if not isinstance(attribute, moderngl.Attribute):
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


class ShaderSource:
    """
    Helper class to deal with shader source files.
    This represents a single shader (vert/frag/geo)
    """
    def __init__(self, type, name, source):
        self.type = type
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
        if self.type == GL.GL_VERTEX_SHADER:
            self.lines.insert(1, "#define VERTEX_SHADER 1")
        elif self.type == GL.GL_FRAGMENT_SHADER:
            self.lines.insert(1, "#define FRAGMENT_SHADER 1")
        elif self.type == GL.GL_GEOMETRY_SHADER:
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

    def type_name(self):
        """Returns a string representation of the shader type"""
        if self.type == GL.GL_VERTEX_SHADER:
            return 'VERTEX_SHADER'
        if self.type == GL.GL_FRAGMENT_SHADER:
            return 'FRAGMENT_SHADER'
        if self.type == GL.GL_GEOMETRY_SHADER:
            return 'GEOMETRY_SHADER'
        else:
            raise ShaderError("Unknown shader type")
