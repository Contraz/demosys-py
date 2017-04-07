import os
from OpenGL import GL


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
        GL.glUseProgram(self.program)

    def set_source(self, source):
        """Define a single source file"""
        self.set_vertex_source(source)
        self.set_fragment_source(source)
        # TODO: This needs to be solved in a better way
        if 'GEOMETRY_SHADER' in source:
            self.set_geometry_source(source)

    def set_vertex_source(self, source):
        self.vert_source = ShaderSource(GL.GL_VERTEX_SHADER, self.name, source)

    def set_fragment_source(self, source):
        self.frag_source = ShaderSource(GL.GL_FRAGMENT_SHADER, self.name, source)

    def set_geometry_source(self, source):
        self.geo_source = ShaderSource(GL.GL_GEOMETRY_SHADER, self.name, source)

    def prepare(self):
        # check version ..
        self.vert_source.compile()
        self.frag_source.compile()
        if self.geo_source:
            self.geo_source.compile()
        self.link()
        self.build_uniform_map()
        self.build_attribute_map()

    def link(self):
        self.program = GL.glCreateProgram()
        GL.glAttachShader(self.program, self.vert_source.shader)
        GL.glAttachShader(self.program, self.frag_source.shader)
        if self.geo_source:
            GL.glAttachShader(self.program, self.geo_source.shader)
        GL.glLinkProgram(self.program)
        status = GL.glGetProgramiv(self.program, GL.GL_LINK_STATUS)
        if not status:
            message = GL.glGetShaderInfoLog(self.program)
            print("M:", message)
            raise ShaderError("Failed to link shader {}: {}".format(self.name, message))

    def build_uniform_map(self):
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
        """Get the uniform location"""
        uniform = self.uniform_map.get(name)
        if not uniform:
            raise ShaderError("Uniform '{}' not found in shader {}".format(name, self.name))
        return uniform

    def uniform_check(self, name, expected_type):
        """Get a uniform and verify the expected type"""
        uniform = self.uniform(name)
        if uniform.type.value != expected_type:
            raise ShaderError("Incorrect data type: Uniform '{}' is of type {}".format(name, uniform.type.name))
        return uniform

    # --- Setting uniforms ---

    def uniform_1f(self, name, value):
        """Set a float uniform"""
        uniform = self.uniform_check(name, GL.GL_FLOAT)
        GL.glUniform1f(uniform.location, value)

    def uniform_2f(self, name, x, y):
        """Set a float uniform"""
        uniform = self.uniform_check(name, GL.GL_FLOAT_VEC2)
        GL.glUniform2f(uniform.location, x, y)

    def uniform_3f(self, name, x, y, z):
        """Set a float uniform"""
        uniform = self.uniform_check(name, GL.GL_FLOAT_VEC3)
        GL.glUniform3f(uniform.location, x, y, z)

    def uniform_4f(self, name, x, y, z, w):
        """Set a vec4 uniform"""
        uniform = self.uniform_check(name, GL.GL_FLOAT_VEC4)
        GL.glUniform4f(uniform.location, x, y, z, w)

    # --- Matrices ---

    def uniform_mat3(self, name, mat):
        """Set a mat3 uniform"""
        if mat is None:
            raise ShaderError("Attempted to set uniform to None")
        uniform = self.uniform_check(name, GL.GL_FLOAT_MAT3)
        GL.glUniformMatrix3fv(uniform.location, 1, GL.GL_FALSE, mat)

    def uniform_mat4(self, name, mat):
        """Set a mat4 uniform"""
        if mat is None:
            raise ShaderError("Attempted to set uniform to None")
        uniform = self.uniform_check(name, GL.GL_FLOAT_MAT4)
        GL.glUniformMatrix4fv(uniform.location, 1, GL.GL_FALSE, mat)

    # --- Sampler ---

    def uniform_sampler_2d(self, unit, name, texture):
        uniform = self.uniform(name)
        GL.glActiveTexture(GL.GL_TEXTURE0 + unit)
        texture.bind()
        GL.glUniform1i(uniform.location, unit)

    def uniform_sampler_1d(self, unit, name, texture):
        uniform = self.uniform(name)
        GL.glActiveTexture(GL.GL_TEXTURE0 + unit)
        texture.bind()
        GL.glUniform1i(uniform.location, unit)


class ShaderSource:
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
        self.shader = GL.glCreateShader(self.type)
        GL.glShaderSource(self.shader, self.source)
        GL.glCompileShader(self.shader)
        message = GL.glGetShaderInfoLog(self.shader)
        if message:
            self.print()
            raise ShaderError("Failed to compile {} {}: {}".format(self.type_name(), self.name, message.decode()))

    def print(self):
        print("---[ START {} ]---".format(self.name))
        for i, line in enumerate(self.lines):
            print("{}: {}".format(str(i).zfill(3), line))
        print("---[ END {} ]---".format(self.name))

    def type_name(self):
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
