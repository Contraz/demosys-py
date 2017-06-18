import os
from OpenGL import GL
import ctypes


class ShaderError(Exception):
    pass


class Uniform:
    """Stores information about a uniform"""
    def __init__(self, name, size, type, location):
        """
        :param name: Name of the uniform
        :param size: Size if the uniform (1 if not an array)
        :param type: Data type of a uniform
        """
        self.name = name.decode()
        self.size = size
        type_info = TYPE_INFO.get(type)
        if not type_info:
            raise ShaderError("Uniform type {} not supported".format(self.type.name))
        self.type = type_info
        self.location = location

    def __repr__(self):
        return "Uniform[{}] {}[{}] {} ({})".format(self.location, self.name, self.size, self.type.name, self.type.value)


class Attribute:
    """Stores information about a shader attribute"""
    def __init__(self, name, type, location):
        """
        :param name: Name of the attribute
        :param type: Data type of the attribute
        :param location: Location in the shader
        """
        self.name = name.decode()
        self.location = location
        type_info = TYPE_INFO.get(type)
        if not type_info:
            raise ShaderError("Attribute type {} not supported".format(self.type.name))
        self.type = type_info

    def __repr__(self):
        return "Attribute[{}] {} {} ({})".format(self.location, self.name, self.type.name, self.type.value)


class Shader:
    """
    Represents a shader program
    """
    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path)
        self.vert_source = None
        self.frag_source = None
        self.geo_source = None
        self.program = None
        # Shader inputs
        self.uniform_map = {}

        self.attribute_list = []
        self.attribute_map = {}
        # A string of concatenated attribute names
        self.attribute_key = None

    def bind(self):
        """
        Bind the shader
        """
        GL.glUseProgram(self.program)

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
        self.vert_source = ShaderSource(GL.GL_VERTEX_SHADER, self.name, source)

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
        # Attempt to delete the current shader in case we are re-loading
        self.delete()

        # Compile the separate shaders
        self.vert_source.compile()

        if self.geo_source:
            self.geo_source.compile()

        if self.frag_source:
            self.frag_source.compile()

        self.link()

        # Build internal lookups
        self.build_uniform_map()
        self.build_attribute_map()

        # We only need the programs for linking
        if self.vert_source:
            self.vert_source.delete(self.program)
        if self.frag_source:
            self.frag_source.delete(self.program)
        if self.geo_source:
            self.geo_source.delete(self.program)

    def delete(self):
        """Frees the memory and invalidates the name associated with the program"""
        if self.program:
            GL.glDeleteProgram(self.program)

    def link(self):
        """
        Links the program.
        Raises ``ShaderError`` if the linker failed.
        """
        self.program = GL.glCreateProgram()
        GL.glAttachShader(self.program, self.vert_source.shader)

        if self.geo_source:
            GL.glAttachShader(self.program, self.geo_source.shader)

        if self.frag_source:
            GL.glAttachShader(self.program, self.frag_source.shader)

        # If no fragment shader is present we are dealing with transform feedback
        if not self.frag_source:
            # Find out attributes
            # Out attribs is present in geometry shader if present
            if self.geo_source:
                out_attribs = self.geo_source.find_out_attribs()
            # Otherwise they are specified in vertex shader
            else:
                out_attribs = self.vert_source.find_out_attribs()

            print("Transform feedback attribs:", out_attribs)

            # Prepare ctypes data containing attrib names
            array_type = ctypes.c_char_p * len(out_attribs)
            buff = array_type()
            for i, e in enumerate(out_attribs):
                buff[i] = e.encode()

            c_text = ctypes.cast(ctypes.pointer(buff), ctypes.POINTER(ctypes.POINTER(GL.GLchar)))
            GL.glTransformFeedbackVaryings(self.program, len(out_attribs), c_text, GL.GL_INTERLEAVED_ATTRIBS)

        GL.glLinkProgram(self.program)

        status = GL.glGetProgramiv(self.program, GL.GL_LINK_STATUS)
        if not status:
            message = GL.glGetProgramInfoLog(self.program)
            print("M:", message)
            raise ShaderError("Failed to link shader {}: {}".format(self.name, message))

    def build_uniform_map(self):
        """
        Builds an internal uniform map by querying the program.
        This way we don't have to query OpenGL (can cause slowdowns)
        """
        uniform_count = GL.glGetProgramiv(self.program, GL.GL_ACTIVE_UNIFORMS)
        print("Shader {} has {} uniform(s)".format(self.name, uniform_count))
        for i in range(uniform_count):
            info = GL.glGetActiveUniform(self.program, i)
            # Get the actual location of the uniform as types over a certain size span several locations
            location = GL.glGetUniformLocation(self.program, info[0])
            uniform = Uniform(info[0], info[1], info[2], location)
            self.uniform_map[uniform.name] = uniform
            print(" - {}".format(uniform))

    def build_attribute_map(self):
        """
        Builds an internal attribute map by querying the program.
        This way we don't have to query OpenGL (can cause slowdowns)
        This information is also used when the shader and VAO negotiates the buffer binding.
        """
        attribute_count = GL.glGetProgramiv(self.program, GL.GL_ACTIVE_ATTRIBUTES)
        bufsize = GL.glGetProgramiv(self.program, GL.GL_ACTIVE_ATTRIBUTE_MAX_LENGTH)
        print("Shader {} has {} attribute(s)".format(self.name, attribute_count))
        for i in range(attribute_count):
            # Unlike glGetActiveUniform the attrib version do not return a convenient tuple
            # and we'll have to use to ugly version. (Most people make wrappers for this one)
            length, size, type, name = GL.GLsizei(), GL.GLint(), GL.GLenum(), (GL.GLchar * bufsize)()
            GL.glGetActiveAttrib(self.program, i, bufsize, length, size, type, name)

            # Get the actual location. Do not trust the original order
            location = GL.glGetAttribLocation(self.program, name.value)
            attribute = Attribute(name.value, type.value, location)
            self.attribute_map[attribute.name] = attribute
            self.attribute_list.append(attribute)
            print(" - {}".format(attribute))

        self.attribute_key = ','.join(name for name in sorted(self.attribute_map.keys()))
        print("Shader attribute key:", self.attribute_key)

    def uniform(self, name):
        """
        Get the uniform location.
        Raises ``ShaderError`` if the uniform is not found.

        :param name: The name of the uniform
        :return: Uniform object
        """
        uniform = self.uniform_map.get(name)
        if not uniform:
            raise ShaderError("Uniform '{}' not found in shader {}".format(name, self.name))
        return uniform

    def uniform_check(self, name, expected_type):
        """
        Get a uniform and verify the expected type.
        This is used by the ``uniform_*`` methods for validating the actual type in the shader
        and the uniform we are trying to set.
        Raises ``ShaderError`` if the uniform is not found.

        :param name: The name of the uniform
        :param expected_type: The expected type of the uniform.
        :return: The Uniform object
        """
        uniform = self.uniform(name)
        if uniform.type.value != expected_type:
            raise ShaderError("Incorrect data type: Uniform '{}' is of type {}".format(name, uniform.type.name))
        return uniform

    # --- Float uniforms ---

    def uniform_1f(self, name, value):
        """
        Set a float uniform

        :param name: Name of the uniform
        :param value: float value
        """
        uniform = self.uniform_check(name, GL.GL_FLOAT)
        GL.glUniform1f(uniform.location, value)

    def uniform_2f(self, name, x, y):
        """
        Set a vec2 uniform

        :param name: name of the uniform
        :param x: float value
        :param y: float value
        """
        uniform = self.uniform_check(name, GL.GL_FLOAT_VEC2)
        GL.glUniform2f(uniform.location, x, y)

    def uniform_3f(self, name, x, y, z):
        """
        Set a vec3 uniform

        :param name: Name of the uniform
        :param x: float value
        :param y: float value
        :param z: float value
        """
        uniform = self.uniform_check(name, GL.GL_FLOAT_VEC3)
        GL.glUniform3f(uniform.location, x, y, z)

    def uniform_4f(self, name, x, y, z, w):
        """
        Set a vec4 uniform

        :param name: Name of the uniform
        :param x: float value
        :param y: float value
        :param z: float value
        :param w: float value
        """
        uniform = self.uniform_check(name, GL.GL_FLOAT_VEC4)
        GL.glUniform4f(uniform.location, x, y, z, w)

    # --- Float uniform arrays ---

    def uniform_1fv(self, name, value, count=1):
        """
        Set a float uniform

        :param name: Name of the uniform
        :param count: Length of the uniform array (default 1)
        :param value: float array
        """
        uniform = self.uniform_check(name, GL.GL_FLOAT)
        GL.glUniform1fv(uniform.location, count, value)

    def uniform_2fv(self, name, value, count=1):
        """
        Set a vec2 uniform

        :param name: name of the uniform
        :param count: Length of the uniform array (default 1)
        :param value: float array
        """
        uniform = self.uniform_check(name, GL.GL_FLOAT_VEC2)
        GL.glUniform2fv(uniform.location, count, value)

    def uniform_3fv(self, name, value, count=1):
        """
        Set a vec3 uniform

        :param name: Name of the uniform
        :param count: Length of the uniform array (default 1)
        :param value: float array
        """
        uniform = self.uniform_check(name, GL.GL_FLOAT_VEC3)
        GL.glUniform3fv(uniform.location, count, value)

    def uniform_4fv(self, name, value, count=1):
        """
        Set a vec4 uniform

        :param name: Name of the uniform
        :param count: Length of the uniform array (default 1)
        :param value: float array
        """
        uniform = self.uniform_check(name, GL.GL_FLOAT_VEC4)
        GL.glUniform4fv(uniform.location, count, value)

    # --- Double precision floats ---

    def uniform_1d(self, name, value):
        """
        Set a double uniform

        :param name: Name of the uniform
        :param value: double value
        """
        uniform = self.uniform_check(name, GL.GL_DOUBLE)
        GL.glUniform1d(uniform.location, value)

    def uniform_2d(self, name, x, y):
        """
        Set a dvec2 uniform

        :param name: name of the uniform
        :param x: double value
        :param y: double value
        """
        uniform = self.uniform_check(name, GL.GL_DOUBLE_VEC2)
        GL.glUniform2d(uniform.location, x, y)

    def uniform_3d(self, name, x, y, z):
        """
        Set a dvec3 uniform

        :param name: Name of the uniform
        :param x: double value
        :param y: double value
        :param z: double value
        """
        uniform = self.uniform_check(name, GL.GL_DOUBLE_VEC3)
        GL.glUniform3d(uniform.location, x, y, z)

    def uniform_4d(self, name, x, y, z, w):
        """
        Set a dvec4 uniform

        :param name: Name of the uniform
        :param x: double value
        :param y: double value
        :param z: double value
        :param w: double value
        """
        uniform = self.uniform_check(name, GL.GL_DOUBLE_VEC4)
        GL.glUniform4d(uniform.location, x, y, z, w)

    # --- Double precision floats arrays ---

    def uniform_1dv(self, name, value, count=1):
        """
        Set a double uniform

        :param name: Name of the uniform
        :param value: float array
        :param count: Length of the uniform array (default 1)
        """
        uniform = self.uniform_check(name, GL.GL_DOUBLE)
        GL.glUniform1dv(uniform.location, count, value)

    def uniform_2dv(self, name, value, count=1):
        """
        Set a dvec2 uniform

        :param name: name of the uniform
        :param value: float array
        :param count: Length of the uniform array (default 1)
        """
        uniform = self.uniform_check(name, GL.GL_DOUBLE_VEC2)
        GL.glUniform2dv(uniform.location, count, value)

    def uniform_3dv(self, name, value, count=1):
        """
        Set a dvec3 uniform

        :param name: Name of the uniform
        :param value: float array
        :param count: Length of the uniform array (default 1)
        """
        uniform = self.uniform_check(name, GL.GL_DOUBLE_VEC3)
        GL.glUniform3dv(uniform.location, count, value)

    def uniform_4dv(self, name, value, count=1):
        """
        Set a dvec4 uniform

        :param name: Name of the uniform
        :param value: float array
        :param count: Length of the uniform array (default 1)
        """
        uniform = self.uniform_check(name, GL.GL_DOUBLE_VEC4)
        GL.glUniform4dv(uniform.location, count, value)

    # --- Signed Integers ---

    def uniform_1i(self, name, value):
        """
        Sets an int

        :param name: Name of the uniform
        :param value: Integer value
        """
        uniform = self.uniform_check(name, GL.GL_INT)
        GL.glUniform1i(uniform.location, value)

    def uniform_2i(self, name, x, y):
        """
        Sets an ivec2

        :param name: Uniform name
        :param x: Integer
        :param y: Integer
        """
        uniform = self.uniform_check(name, GL.GL_INT_VEC2)
        GL.glUniform2i(uniform.location, x, y)

    def uniform_3i(self, name, x, y, z):
        """
        Sets an ivec3

        :param name: Uniform name
        :param x: Integer
        :param y: Integer
        :param z: Integer
        """
        uniform = self.uniform_check(name, GL.GL_INT_VEC3)
        GL.glUniform3i(uniform.location, x, y, z)

    def uniform_4i(self, name, x, y, z, w):
        """
        Sets an ivec4

        :param name: Uniform name
        :param x: Integer
        :param y: Integer
        :param z: Integer
        :param w: Integer
        """
        uniform = self.uniform_check(name, GL.GL_INT_VEC4)
        GL.glUniform4i(uniform.location, x, y, z, w)

    # --- Signed Integers Arrays ---

    def uniform_1iv(self, name, value, count=1):
        """
        Sets an int

        :param name: Name of the uniform
        :param value: integer array
        :param count: Length of the uniform array (default 1)
        """
        uniform = self.uniform_check(name, GL.GL_INT)
        GL.glUniform1iv(uniform.location, count, value)

    def uniform_2iv(self, name, value, count=1):
        """
        Sets an ivec2

        :param name: Uniform name
        :param value: integer array
        :param count: Length of the uniform array (default 1)
        """
        uniform = self.uniform_check(name, GL.GL_INT_VEC2)
        GL.glUniform2iv(uniform.location, count, value)

    def uniform_3iv(self, name, value, count=1):
        """
        Sets an ivec3

        :param name: Uniform name
        :param value: integer array
        :param count: Length of the uniform array (default 1)
        """
        uniform = self.uniform_check(name, GL.GL_INT_VEC3)
        GL.glUniform3iv(uniform.location, count, value)

    def uniform_4iv(self, name, value, count=1):
        """
        Sets an ivec4

        :param name: Uniform name
        :param value: integer array
        :param count: Length of the uniform array (default 1)
        """
        uniform = self.uniform_check(name, GL.GL_INT_VEC4)
        GL.glUniform4iv(uniform.location, count, value)

    # --- Unsigned Integers ---

    def uniform_1ui(self, name, value):
        """
        Sets an uint

        :param name: Name of the uniform
        :param value: Integer value
        """
        uniform = self.uniform_check(name, GL.GL_UNSIGNED_INT)
        GL.glUniform1ui(uniform.location, value)

    def uniform_2ui(self, name, x, y):
        """
        Sets an uvec2

        :param name: Uniform name
        :param x: Integer
        :param y: Integer
        """
        uniform = self.uniform_check(name, GL.GL_UNSIGNED_INT_VEC2)
        GL.glUniform2ui(uniform.location, x, y)

    def uniform_3ui(self, name, x, y, z):
        """
        Sets an uvec3

        :param name: Uniform name
        :param x: Integer
        :param y: Integer
        :param z: Integer
        """
        uniform = self.uniform_check(name, GL.GL_UNSIGNED_INT_VEC3)
        GL.glUniform3ui(uniform.location, x, y, z)

    def uniform_4ui(self, name, x, y, z, w):
        """
        Sets an uvec4

        :param name: Uniform name
        :param x: Integer
        :param y: Integer
        :param z: Integer
        :param w: Integer
        """
        uniform = self.uniform_check(name, GL.GL_UNSIGNED_INT_VEC4)
        GL.glUniform4ui(uniform.location, x, y, z, w)

    # --- Unsigned Integer Arrays ---

    def uniform_1uiv(self, name, value, count=1):
        """
        Sets an uint

        :param name: Name of the uniform
        :param value: integer array
        :param count: Length of the uniform array (default 1)
        """
        uniform = self.uniform_check(name, GL.GL_UNSIGNED_INT)
        GL.glUniform1uiv(uniform.location, count, value)

    def uniform_2uiv(self, name, value, count=1):
        """
        Sets an uvec2

        :param name: Uniform name
        :param value: integer array
        :param count: Length of the uniform array (default 1)
        """
        uniform = self.uniform_check(name, GL.GL_UNSIGNED_INT_VEC2)
        GL.glUniform2uiv(uniform.location, count, value)

    def uniform_3uiv(self, name, value, count=1):
        """
        Sets an uvec3

        :param name: Uniform name
        :param value: integer array
        :param count: Length of the uniform array (default 1)
        """
        uniform = self.uniform_check(name, GL.GL_UNSIGNED_INT_VEC3)
        GL.glUniform3uiv(uniform.location, count, value)

    def uniform_4uiv(self, name, value, count=1):
        """
        Sets an uvec4

        :param name: Uniform name
        :param value: integer array
        :param count: Length of the uniform array (default 1)
        """
        uniform = self.uniform_check(name, GL.GL_UNSIGNED_INT_VEC4)
        GL.glUniform4uiv(uniform.location, count, value)

    # --- Booleans ---

    def uniform_1b(self, name, value):
        """
        Sets an bool

        :param name: Name of the uniform
        :param value: Integer value
        """
        uniform = self.uniform_check(name, GL.GL_BOOL)
        GL.glUniform1i(uniform.location, value)

    def uniform_2b(self, name, x, y):
        """
        Sets an bvec2

        :param name: Uniform name
        :param x: bool
        :param y: bool
        """
        uniform = self.uniform_check(name, GL.GL_BOOL_VEC2)
        GL.glUniform2i(uniform.location, x, y)

    def uniform_3b(self, name, x, y, z):
        """
        Sets an bvec3

        :param name: Uniform name
        :param x: bool
        :param y: bool
        :param z: bool
        """
        uniform = self.uniform_check(name, GL.GL_BOOL_VEC3)
        GL.glUniform3i(uniform.location, x, y, z)

    def uniform_4b(self, name, x, y, z, w):
        """
        Sets an bvec4

        :param name: Uniform name
        :param x: bool
        :param y: bool
        :param z: bool
        :param w: bool
        """
        uniform = self.uniform_check(name, GL.GL_BOOL_VEC4)
        GL.glUniform4i(uniform.location, x, y, z, w)

    # --- Matrices ---

    def uniform_mat2(self, name, mat, transpose=GL.GL_FALSE):
        """
        Sets a mat3 uniform

        :param name: Name of the uniform
        :param mat: matrix
        :param transpose: Traspose the matrix
        """
        if mat is None:
            raise ShaderError("Attempted to set uniform to None")
        uniform = self.uniform_check(name, GL.GL_FLOAT_MAT2)
        GL.glUniformMatrix2fv(uniform.location, 1, transpose, mat)

    def uniform_mat3(self, name, mat, transpose=GL.GL_FALSE):
        """
        Sets a mat3 uniform

        :param name: Name of the uniform
        :param mat: matrix
        :param transpose: Traspose the matrix
        """
        if mat is None:
            raise ShaderError("Attempted to set uniform to None")
        uniform = self.uniform_check(name, GL.GL_FLOAT_MAT3)
        GL.glUniformMatrix3fv(uniform.location, 1, transpose, mat)

    def uniform_mat4(self, name, mat, transpose=GL.GL_FALSE):
        """
        Set a mat4 uniform

        :param name: Name of the uniform
        :param mat: matrix
        """
        if mat is None:
            raise ShaderError("Attempted to set uniform to None")
        uniform = self.uniform_check(name, GL.GL_FLOAT_MAT4)
        GL.glUniformMatrix4fv(uniform.location, 1, transpose, mat)

    # --- Sampler ---

    def uniform_sampler_1d(self, unit, name, texture):
        """
        Sets a sampler1d

        :param unit: The texture unit to use (0 - N)
        :param name: Name of the uniform
        :param texture: The Texture object
        """
        uniform = self.uniform(name)
        GL.glActiveTexture(GL.GL_TEXTURE0 + unit)
        texture.bind()
        GL.glUniform1i(uniform.location, unit)

    def uniform_sampler_2d(self, unit, name, texture):
        """
        Sets a sampler2d

        :param unit: The texture unit to use (0 - N)
        :param name: Name of the uniform
        :param texture: The Texture object
        """
        uniform = self.uniform(name)
        GL.glActiveTexture(GL.GL_TEXTURE0 + unit)
        texture.bind()
        GL.glUniform1i(uniform.location, unit)

    def uniform_sampler_3d(self, unit, name, texture):
        """
        Sets a sampler3d

        :param unit: The texture unit to use (0 - N)
        :param name: Name of the uniform
        :param texture: The Texture object
        """
        uniform = self.uniform(name)
        GL.glActiveTexture(GL.GL_TEXTURE0 + unit)
        texture.bind()
        GL.glUniform1i(uniform.location, unit)


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

    def compile(self):
        """Compile the shader"""
        self.shader = GL.glCreateShader(self.type)
        GL.glShaderSource(self.shader, self.source)
        GL.glCompileShader(self.shader)
        message = GL.glGetShaderInfoLog(self.shader)
        if message:
            self.print()
            raise ShaderError("Failed to compile {} {}: {}".format(self.type_name(), self.name, message.decode()))

    def delete(self, program=None):
        """Frees the memory and invalidates the name associated with the shader object """
        # The shader will not be deleted if attached
        if program:
            GL.glDetachShader(program, self.shader)
        # Now we can delete it
        GL.glDeleteShader(self.shader)

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


SIZE_OF_FLOAT = 4
SIZE_OF_DOUBLE = 8
SIZE_OF_INT = 4


class TypeInfo:
    """
    Information about a data type in a glsl shader.

    Example: "GL_FLOAT_VEC3" is a GL.GL_FLOAT_VEC3 of byte size 12
    """
    def __init__(self, name, value, size):
        """
        :param name: Name of the type (ex 'GL_FLOAT_VEC4')
        :param value: Enum value in OpenGL
        :param size:  Size in bytes
        """
        self.name = name
        self.value = value
        self.size = size


# Information about data types
# TODO: May contain deprecated types. Needs cleanup.
# TODO: Types may be missing past GL 3.3
TYPE_INFO = {
    # Floats
    GL.GL_FLOAT: TypeInfo("GL_FLOAT", GL.GL_FLOAT, SIZE_OF_FLOAT),
    GL.GL_FLOAT_VEC2: TypeInfo("GL_FLOAT_VEC2", GL.GL_FLOAT_VEC2, SIZE_OF_FLOAT * 2),
    GL.GL_FLOAT_VEC3: TypeInfo("GL_FLOAT_VEC3", GL.GL_FLOAT_VEC3, SIZE_OF_FLOAT * 3),
    GL.GL_FLOAT_VEC4: TypeInfo("GL_FLOAT_VEC4", GL.GL_FLOAT_VEC4, SIZE_OF_FLOAT * 3),
    # Doubles
    GL.GL_DOUBLE: TypeInfo("GL_DOUBLE", GL.GL_DOUBLE, SIZE_OF_DOUBLE),
    GL.GL_DOUBLE_VEC2: TypeInfo("GL_DOUBLE_VEC2", GL.GL_DOUBLE_VEC2, SIZE_OF_DOUBLE * 2),
    GL.GL_DOUBLE_VEC3: TypeInfo("GL_DOUBLE_VEC3", GL.GL_DOUBLE_VEC3, SIZE_OF_DOUBLE * 3),
    GL.GL_DOUBLE_VEC4: TypeInfo("GL_DOUBLE_VEC4", GL.GL_DOUBLE_VEC4, SIZE_OF_DOUBLE * 4),
    # Samplers
    GL.GL_SAMPLER_1D: TypeInfo("GL_SAMPLER_1D", GL.GL_SAMPLER_1D, SIZE_OF_INT),
    GL.GL_SAMPLER_2D: TypeInfo("GL_SAMPLER_2D", GL.GL_SAMPLER_2D, SIZE_OF_INT),
    GL.GL_SAMPLER_3D: TypeInfo("GL_SAMPLER_3D", GL.GL_SAMPLER_3D, SIZE_OF_INT),
    GL.GL_SAMPLER_CUBE: TypeInfo("GL_SAMPLER_CUBE", GL.GL_SAMPLER_CUBE, SIZE_OF_INT),
    GL.GL_SAMPLER_1D_SHADOW: TypeInfo("GL_SAMPLER_1D_SHADOW", GL.GL_SAMPLER_CUBE, SIZE_OF_INT),
    GL.GL_SAMPLER_2D_SHADOW: TypeInfo("GL_SAMPLER_2D_SHADOW", GL.GL_SAMPLER_2D_SHADOW, SIZE_OF_INT),
    GL.GL_SAMPLER_1D_ARRAY: TypeInfo("GL_SAMPLER_1D_ARRAY", GL.GL_SAMPLER_1D_ARRAY, SIZE_OF_INT),
    GL.GL_SAMPLER_2D_ARRAY: TypeInfo("GL_SAMPLER_2D_ARRAY", GL.GL_SAMPLER_2D_ARRAY, SIZE_OF_INT),
    GL.GL_SAMPLER_1D_ARRAY_SHADOW: TypeInfo("GL_SAMPLER_1D_ARRAY_SHADOW", GL.GL_SAMPLER_1D_ARRAY_SHADOW, SIZE_OF_INT),
    GL.GL_SAMPLER_2D_ARRAY_SHADOW: TypeInfo("GL_SAMPLER_2D_ARRAY_SHADOW", GL.GL_SAMPLER_2D_ARRAY_SHADOW, SIZE_OF_INT),
    GL.GL_SAMPLER_2D_MULTISAMPLE: TypeInfo("GL_SAMPLER_2D_MULTISAMPLE", GL.GL_SAMPLER_2D_MULTISAMPLE, SIZE_OF_INT),
    GL.GL_SAMPLER_2D_MULTISAMPLE_ARRAY: TypeInfo("GL_SAMPLER_2D_MULTISAMPLE_ARRAY", GL.GL_SAMPLER_2D_MULTISAMPLE_ARRAY,
                                                 SIZE_OF_INT),
    GL.GL_SAMPLER_CUBE_SHADOW: TypeInfo("GL_SAMPLER_CUBE_SHADOW", GL.GL_SAMPLER_CUBE_SHADOW, SIZE_OF_INT),
    GL.GL_SAMPLER_BUFFER: TypeInfo("GL_SAMPLER_BUFFER", GL.GL_SAMPLER_BUFFER, SIZE_OF_INT),
    GL.GL_SAMPLER_2D_RECT: TypeInfo("GL_SAMPLER_2D_RECT", GL.GL_SAMPLER_2D_RECT, SIZE_OF_INT),
    GL.GL_SAMPLER_2D_RECT_SHADOW: TypeInfo("GL_SAMPLER_2D_RECT_SHADOW", GL.GL_SAMPLER_2D_RECT_SHADOW, SIZE_OF_INT),
    # Integer samplers
    GL.GL_INT_SAMPLER_1D: TypeInfo("GL_INT_SAMPLER_1D", GL.GL_INT_SAMPLER_1D, SIZE_OF_INT),
    GL.GL_INT_SAMPLER_2D: TypeInfo("GL_INT_SAMPLER_2D", GL.GL_INT_SAMPLER_2D, SIZE_OF_INT),
    GL.GL_INT_SAMPLER_3D: TypeInfo("GL_INT_SAMPLER_3D", GL.GL_INT_SAMPLER_3D, SIZE_OF_INT),
    GL.GL_INT_SAMPLER_CUBE: TypeInfo("GL_INT_SAMPLER_CUBE", GL.GL_INT_SAMPLER_CUBE, SIZE_OF_INT),
    GL.GL_INT_SAMPLER_1D_ARRAY: TypeInfo("GL_INT_SAMPLER_1D_ARRAY", GL.GL_INT_SAMPLER_1D_ARRAY, SIZE_OF_INT),
    GL.GL_INT_SAMPLER_2D_ARRAY: TypeInfo("GL_INT_SAMPLER_2D_ARRAY", GL.GL_INT_SAMPLER_2D_ARRAY, SIZE_OF_INT),
    GL.GL_INT_SAMPLER_2D_MULTISAMPLE: TypeInfo("GL_INT_SAMPLER_2D_MULTISAMPLE", GL.GL_INT_SAMPLER_2D_MULTISAMPLE,
                                               SIZE_OF_INT),
    GL.GL_INT_SAMPLER_2D_MULTISAMPLE_ARRAY: TypeInfo("GL_INT_SAMPLER_2D_MULTISAMPLE_ARRAY",
                                                     GL.GL_INT_SAMPLER_2D_MULTISAMPLE_ARRAY, SIZE_OF_INT),
    GL.GL_INT_SAMPLER_BUFFER: TypeInfo("GL_INT_SAMPLER_BUFFER", GL.GL_INT_SAMPLER_BUFFER, SIZE_OF_INT),
    GL.GL_INT_SAMPLER_2D_RECT: TypeInfo("GL_INT_SAMPLER_2D_RECT", GL.GL_INT_SAMPLER_2D_RECT, SIZE_OF_INT),
    # Unsigned integer samplers
    GL.GL_UNSIGNED_INT_SAMPLER_1D: TypeInfo("GL_UNSIGNED_INT_SAMPLER_1D", GL.GL_UNSIGNED_INT_SAMPLER_1D, SIZE_OF_INT),
    GL.GL_UNSIGNED_INT_SAMPLER_2D: TypeInfo("GL_UNSIGNED_INT_SAMPLER_2D", GL.GL_UNSIGNED_INT_SAMPLER_2D, SIZE_OF_INT),
    GL.GL_UNSIGNED_INT_SAMPLER_3D: TypeInfo("GL_UNSIGNED_INT_SAMPLER_3D", GL.GL_UNSIGNED_INT_SAMPLER_3D, SIZE_OF_INT),
    GL.GL_UNSIGNED_INT_SAMPLER_CUBE: TypeInfo("GL_UNSIGNED_INT_SAMPLER_CUBE", GL.GL_UNSIGNED_INT_SAMPLER_CUBE,
                                              SIZE_OF_INT),
    GL.GL_UNSIGNED_INT_SAMPLER_1D_ARRAY: TypeInfo("GL_UNSIGNED_INT_SAMPLER_1D_ARRAY",
                                                  GL.GL_UNSIGNED_INT_SAMPLER_1D_ARRAY, SIZE_OF_INT),
    GL.GL_UNSIGNED_INT_SAMPLER_2D_ARRAY: TypeInfo("GL_UNSIGNED_INT_SAMPLER_2D_ARRAY",
                                                  GL.GL_UNSIGNED_INT_SAMPLER_2D_ARRAY, SIZE_OF_INT),
    GL.GL_UNSIGNED_INT_SAMPLER_2D_MULTISAMPLE: TypeInfo("GL_UNSIGNED_INT_SAMPLER_2D_MULTISAMPLE",
                                                        GL.GL_UNSIGNED_INT_SAMPLER_2D_MULTISAMPLE, SIZE_OF_INT),
    GL.GL_UNSIGNED_INT_SAMPLER_2D_MULTISAMPLE_ARRAY: TypeInfo("GL_UNSIGNED_INT_SAMPLER_2D_MULTISAMPLE_ARRAY",
                                                              GL.GL_UNSIGNED_INT_SAMPLER_2D_MULTISAMPLE_ARRAY,
                                                              SIZE_OF_INT),
    GL.GL_UNSIGNED_INT_SAMPLER_BUFFER: TypeInfo("GL_UNSIGNED_INT_SAMPLER_BUFFER",
                                                GL.GL_UNSIGNED_INT_SAMPLER_BUFFER, SIZE_OF_INT),
    GL.GL_UNSIGNED_INT_SAMPLER_2D_RECT: TypeInfo("GL_UNSIGNED_INT_SAMPLER_2D_RECT",
                                                 GL.GL_UNSIGNED_INT_SAMPLER_2D_RECT, SIZE_OF_INT),
    # Booleans
    GL.GL_BOOL: TypeInfo("GL_BOOL", GL.GL_BOOL, SIZE_OF_INT),
    GL.GL_BOOL_VEC2: TypeInfo("GL_BOOL_VEC2", GL.GL_BOOL_VEC2, SIZE_OF_INT * 2),
    GL.GL_BOOL_VEC3: TypeInfo("GL_BOOL_VEC3", GL.GL_BOOL_VEC3, SIZE_OF_INT * 3),
    GL.GL_BOOL_VEC4: TypeInfo("GL_BOOL_VEC4", GL.GL_BOOL_VEC4, SIZE_OF_INT * 4),
    # Integers
    GL.GL_INT: TypeInfo("GL_INT", GL.GL_INT, SIZE_OF_INT),
    GL.GL_INT_VEC2: TypeInfo("GL_INT_VEC2", GL.GL_INT_VEC2, SIZE_OF_INT * 2),
    GL.GL_INT_VEC3: TypeInfo("GL_INT_VEC3", GL.GL_INT_VEC3, SIZE_OF_INT * 3),
    GL.GL_INT_VEC4: TypeInfo("GL_INT_VEC4", GL.GL_INT_VEC4, SIZE_OF_INT * 4),
    # Unsigned Integers
    GL.GL_UNSIGNED_INT: TypeInfo("GL_UNSIGNED_INT", GL.GL_UNSIGNED_INT, SIZE_OF_INT),
    GL.GL_UNSIGNED_INT_VEC2: TypeInfo("GL_UNSIGNED_INT_VEC2", GL.GL_UNSIGNED_INT_VEC2, SIZE_OF_INT * 2),
    GL.GL_UNSIGNED_INT_VEC3: TypeInfo("GL_UNSIGNED_INT_VEC3", GL.GL_UNSIGNED_INT_VEC3, SIZE_OF_INT * 3),
    GL.GL_UNSIGNED_INT_VEC4: TypeInfo("GL_UNSIGNED_INT_VEC4", GL.GL_UNSIGNED_INT_VEC4, SIZE_OF_INT * 4),
    # Byte
    GL.GL_BYTE: TypeInfo("GL_BYTE", GL.GL_BYTE, 1),
    # Matrices (FLOAT)
    GL.GL_FLOAT_MAT2: TypeInfo("GL_FLOAT_MAT2", GL.GL_FLOAT_MAT2, SIZE_OF_FLOAT * 2 * 2),
    GL.GL_FLOAT_MAT3: TypeInfo("GL_FLOAT_MAT3", GL.GL_FLOAT_MAT3, SIZE_OF_FLOAT * 3 * 3),
    GL.GL_FLOAT_MAT4: TypeInfo("GL_FLOAT_MAT4", GL.GL_FLOAT_MAT4, SIZE_OF_FLOAT * 4 * 4),
    GL.GL_FLOAT_MAT2x3: TypeInfo("GL_FLOAT_MAT2x3", GL.GL_FLOAT_MAT2x3, SIZE_OF_FLOAT * 2 * 3),
    GL.GL_FLOAT_MAT2x4: TypeInfo("GL_FLOAT_MAT2x4", GL.GL_FLOAT_MAT2x4, SIZE_OF_FLOAT * 2 * 4),
    GL.GL_FLOAT_MAT3x2: TypeInfo("GL_FLOAT_MAT3x2", GL.GL_FLOAT_MAT3x2, SIZE_OF_FLOAT * 3 * 2),
    GL.GL_FLOAT_MAT3x4: TypeInfo("GL_FLOAT_MAT3x4", GL.GL_FLOAT_MAT3x4, SIZE_OF_FLOAT * 3 * 4),
    GL.GL_FLOAT_MAT4x2: TypeInfo("GL_FLOAT_MAT4x2", GL.GL_FLOAT_MAT4x2, SIZE_OF_FLOAT * 4 * 2),
    GL.GL_FLOAT_MAT4x3: TypeInfo("GL_FLOAT_MAT4x3", GL.GL_FLOAT_MAT4x3, SIZE_OF_FLOAT * 4 * 3),
    # Matrices (DOUBLE)
    GL.GL_DOUBLE_MAT2: TypeInfo("GL_DOUBLE_MAT2", GL.GL_DOUBLE_MAT2, SIZE_OF_DOUBLE * 2 * 2),
    GL.GL_DOUBLE_MAT3: TypeInfo("GL_DOUBLE_MAT3", GL.GL_DOUBLE_MAT3, SIZE_OF_DOUBLE * 3 * 3),
    GL.GL_DOUBLE_MAT4: TypeInfo("GL_DOUBLE_MAT4", GL.GL_DOUBLE_MAT4, SIZE_OF_DOUBLE * 4 * 4),
    GL.GL_DOUBLE_MAT2x3: TypeInfo("GL_DOUBLE_MAT2x3", GL.GL_DOUBLE_MAT2x3, SIZE_OF_DOUBLE * 2 * 3),
    GL.GL_DOUBLE_MAT2x4: TypeInfo("GL_DOUBLE_MAT2x4", GL.GL_DOUBLE_MAT2x4, SIZE_OF_DOUBLE * 2 * 4),
    GL.GL_DOUBLE_MAT3x2: TypeInfo("GL_DOUBLE_MAT3x2", GL.GL_DOUBLE_MAT3x2, SIZE_OF_DOUBLE * 3 * 2),
    GL.GL_DOUBLE_MAT3x4: TypeInfo("GL_DOUBLE_MAT3x4", GL.GL_DOUBLE_MAT3x4, SIZE_OF_DOUBLE * 3 * 4),
    GL.GL_DOUBLE_MAT4x3: TypeInfo("GL_DOUBLE_MAT4x3", GL.GL_DOUBLE_MAT4x3, SIZE_OF_DOUBLE * 4 * 3),
}
