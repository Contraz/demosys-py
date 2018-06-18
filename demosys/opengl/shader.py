import ctypes
import moderngl
import os
from functools import wraps

from OpenGL import GL
from demosys.conf import settings
from .constants import TYPE_INFO
from demosys import context


def uniform_type(uniform_type, name_arg_index=1):
    """
    Checks uniform parameter types and injects uniform instances into uniform methods.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self = args[0]
            uniform = self.uniform_check(args[name_arg_index],
                                         uniform_type,
                                         raise_on_error=settings.SHADER_STRICT_VALIDATION)
            # Only call the actual method if everything is ok
            if uniform:
                kwargs['uniform'] = uniform
                func(*args, **kwargs)
        return wrapper
    return decorator


class ShaderError(Exception):
    pass


# class Uniform:
#     """Stores information about a uniform"""
#     def __init__(self, name, size, type, location):
#         """
#         :param name: Name of the uniform
#         :param size: Size if the uniform (1 if not an array)
#         :param type: Data type of a uniform
#         """
#         self.name = name.decode()
#         self.size = size
#         type_info = TYPE_INFO.get(type)
#
#         if not type_info:
#             raise ShaderError("Uniform type {} not supported".format(self.type.name))
#
#         self.type = type_info
#         self.location = location
#
#     def __repr__(self):
#         return "Uniform[{}] {}[{}] {} ({})".format(
#             self.location, self.name, self.size, self.type.name, self.type.value)


# class Attribute:
#     """Stores information about a shader attribute"""
#     def __init__(self, name, type, location):
#         """
#         :param name: Name of the attribute
#         :param type: Data type of the attribute
#         :param location: Location in the shader
#         """
#         self.name = name.decode()
#         self.location = location
#
#         type_info = TYPE_INFO.get(type)
#
#         if not type_info:
#             raise ShaderError("Attribute type {} not supported".format(self.type.name))
#
#         self.type = type_info
#
#     def __repr__(self):
#         return "Attribute[{}] {} {} ({})".format(self.location, self.name, self.type.name, self.type.value)


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

    def bind(self):
        """
        Bind the shader
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

        # TODO: varyings for transform feedback

        # Raises mgl.Error
        self.program = context.ctx().program(**params)

        # Build internal lookups
        self.build_uniform_map()
        self.build_attribute_map()

    # def delete(self):
    #     """Frees the memory and invalidates the name associated with the program"""
    #     if self.program:
    #         GL.glDeleteProgram(self.program)
    #         self.program = None

    # def link(self):
    #     """
    #     Links the program.
    #     Raises ``ShaderError`` if the linker failed.
    #     """
    #     program = GL.glCreateProgram()
    #     GL.glAttachShader(program, self.vertex_source.shader)
    #
    #     if self.geo_source:
    #         GL.glAttachShader(program, self.geo_source.shader)
    #
    #     if self.frag_source:
    #         GL.glAttachShader(program, self.frag_source.shader)
    #
    #     # If no fragment shader is present we are dealing with transform feedback
    #     if not self.frag_source:
    #         # Find out attributes
    #         # Out attribs is present in geometry shader if present
    #         if self.geo_source:
    #             out_attribs = self.geo_source.find_out_attribs()
    #         # Otherwise they are specified in vertex shader
    #         else:
    #             out_attribs = self.vertex_source.find_out_attribs()
    #
    #         print("Transform feedback attribs:", out_attribs)
    #
    #         # Prepare ctypes data containing attrib names
    #         # array_type = ctypes.c_char_p * len(out_attribs)
    #         # buff = array_type()
    #         # for i, e in enumerate(out_attribs):
    #         #     buff[i] = e.encode()
    #         #
    #         # c_text = ctypes.cast(ctypes.pointer(buff), ctypes.POINTER(ctypes.POINTER(GL.GLchar)))
    #         # GL.glTransformFeedbackVaryings(program, len(out_attribs), c_text, GL.GL_INTERLEAVED_ATTRIBS)
    #
    #     GL.glLinkProgram(program)
    #
    #     status = GL.glGetProgramiv(program, GL.GL_LINK_STATUS)
    #     if not status:
    #         message = GL.glGetProgramInfoLog(program)
    #         print("M:", message)
    #         raise ShaderError("Failed to link shader {}: {}".format(self.name, message))
    #
    #     # Attempt to delete the current shader in case we are re-loading
    #     self.delete()
    #     self.program = program

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

    def uniform(self, name, raise_on_error=True):
        """
        Get the uniform location.
        Raises ``ShaderError`` if the uniform is not found.

        :param name: The name of the uniform
        :param raise_on_error: Raise ShaderError when uniform is not found
        :return: Uniform object
        """
        uniform = self.uniform_map.get(name)

        if not uniform:
            msg = "Uniform '{}' not found in shader {}".format(name, self.name)

            if raise_on_error:
                raise ShaderError(msg)
            else:
                print(msg)
                return None

        return uniform

    def uniform_check(self, name, expected_type, raise_on_error=True):
        """
        Get a uniform and verify the expected type.
        This is used by the ``uniform_*`` methods for validating the actual type in the shader
        and the uniform we are trying to set.
        Raises ``ShaderError`` if the uniform is not found.

        :param name: The name of the uniform
        :param expected_type: The expected type of the uniform.
        :param raise_on_error: Raise ShaderError when uniform do not match type
        :return: The Uniform object
        """
        uniform = self.uniform(name, raise_on_error=raise_on_error)
        if not uniform:
            return None

        # if uniform.type.value != expected_type:
        #     msg = "Incorrect data type: Uniform '{}' is of type {}".format(name, uniform.type.name)
        #
        #     if raise_on_error:
        #         raise ShaderError(msg)
        #     else:
        #         print(msg)
        #         return None

        return uniform

    # --- Float uniforms ---

    @uniform_type(GL.GL_FLOAT)
    def uniform_1f(self, name, value, uniform=None):
        """
        Set a float uniform

        :param name: Name of the uniform
        :param value: float value
        :param uniform: For auto-injection for uniform instance. Do not use.
        """
        GL.glUniform1f(uniform.location, value)

    @uniform_type(GL.GL_FLOAT_VEC2)
    def uniform_2f(self, name, x, y, uniform=None):
        """
        Set a vec2 uniform

        :param name: name of the uniform
        :param x: float value
        :param y: float value
        :param uniform: For auto-injection for uniform instance. Do not use.
        """
        GL.glUniform2f(uniform.location, x, y)

    @uniform_type(GL.GL_FLOAT_VEC3)
    def uniform_3f(self, name, x, y, z, uniform=None):
        """
        Set a vec3 uniform

        :param name: Name of the uniform
        :param x: float value
        :param y: float value
        :param z: float value
        :param uniform: For auto-injection for uniform instance. Do not use.
        """
        GL.glUniform3f(uniform.location, x, y, z)

    @uniform_type(GL.GL_FLOAT_VEC4)
    def uniform_4f(self, name, x, y, z, w, uniform=None):
        """
        Set a vec4 uniform

        :param name: Name of the uniform
        :param x: float value
        :param y: float value
        :param z: float value
        :param w: float value
        :param uniform: For auto-injection for uniform instance. Do not use.
        """
        GL.glUniform4f(uniform.location, x, y, z, w)

    # --- Float uniform arrays ---

    @uniform_type(GL.GL_FLOAT)
    def uniform_1fv(self, name, value, count=1, uniform=None):
        """
        Set a float uniform

        :param name: Name of the uniform
        :param count: Length of the uniform array (default 1)
        :param value: float array
        :param uniform: For auto-injection for uniform instance. Do not use.
        """
        GL.glUniform1fv(uniform.location, count, value)

    @uniform_type(GL.GL_FLOAT_VEC2)
    def uniform_2fv(self, name, value, count=1, uniform=None):
        """
        Set a vec2 uniform

        :param name: name of the uniform
        :param count: Length of the uniform array (default 1)
        :param value: float array
        :param uniform: For auto-injection for uniform instance. Do not use.
        """
        GL.glUniform2fv(uniform.location, count, value)

    @uniform_type(GL.GL_FLOAT_VEC3)
    def uniform_3fv(self, name, value, count=1, uniform=None):
        """
        Set a vec3 uniform

        :param name: Name of the uniform
        :param count: Length of the uniform array (default 1)
        :param value: float array
        :param uniform: For auto-injection for uniform instance. Do not use.
        """
        GL.glUniform3fv(uniform.location, count, value)

    @uniform_type(GL.GL_FLOAT_VEC4)
    def uniform_4fv(self, name, value, count=1, uniform=None):
        """
        Set a vec4 uniform

        :param name: Name of the uniform
        :param count: Length of the uniform array (default 1)
        :param value: float array
        :param uniform: For auto-injection for uniform instance. Do not use.
        """
        GL.glUniform4fv(uniform.location, count, value)

    # --- Double precision floats ---

    @uniform_type(GL.GL_DOUBLE)
    def uniform_1d(self, name, value, uniform=None):
        """
        Set a double uniform

        :param name: Name of the uniform
        :param value: double value
        :param uniform: For auto-injection for uniform instance. Do not use.
        """
        GL.glUniform1d(uniform.location, value)

    @uniform_type(GL.GL_DOUBLE_VEC2)
    def uniform_2d(self, name, x, y, uniform=None):
        """
        Set a dvec2 uniform

        :param name: name of the uniform
        :param x: double value
        :param y: double value
        :param uniform: For auto-injection for uniform instance. Do not use.
        """
        GL.glUniform2d(uniform.location, x, y)

    @uniform_type(GL.GL_DOUBLE_VEC3)
    def uniform_3d(self, name, x, y, z, uniform=None):
        """
        Set a dvec3 uniform

        :param name: Name of the uniform
        :param x: double value
        :param y: double value
        :param z: double value
        :param uniform: For auto-injection for uniform instance. Do not use.
        """
        GL.glUniform3d(uniform.location, x, y, z)

    @uniform_type(GL.GL_DOUBLE_VEC4)
    def uniform_4d(self, name, x, y, z, w, uniform=None):
        """
        Set a dvec4 uniform

        :param name: Name of the uniform
        :param x: double value
        :param y: double value
        :param z: double value
        :param w: double value
        :param uniform: For auto-injection for uniform instance. Do not use.
        """
        GL.glUniform4d(uniform.location, x, y, z, w)

    # --- Double precision floats arrays ---

    @uniform_type(GL.GL_DOUBLE)
    def uniform_1dv(self, name, value, count=1, uniform=None):
        """
        Set a double uniform

        :param name: Name of the uniform
        :param value: float array
        :param count: Length of the uniform array (default 1)
        :param uniform: For auto-injection for uniform instance. Do not use.
        """
        GL.glUniform1dv(uniform.location, count, value)

    @uniform_type(GL.GL_DOUBLE_VEC2)
    def uniform_2dv(self, name, value, count=1, uniform=None):
        """
        Set a dvec2 uniform

        :param name: name of the uniform
        :param value: float array
        :param count: Length of the uniform array (default 1)
        :param uniform: For auto-injection for uniform instance. Do not use.
        """
        GL.glUniform2dv(uniform.location, count, value)

    @uniform_type(GL.GL_DOUBLE_VEC3)
    def uniform_3dv(self, name, value, count=1, uniform=None):
        """
        Set a dvec3 uniform

        :param name: Name of the uniform
        :param value: float array
        :param count: Length of the uniform array (default 1)
        :param uniform: For auto-injection for uniform instance. Do not use.
        """
        GL.glUniform3dv(uniform.location, count, value)

    @uniform_type(GL.GL_DOUBLE_VEC4)
    def uniform_4dv(self, name, value, count=1, uniform=None):
        """
        Set a dvec4 uniform

        :param name: Name of the uniform
        :param value: float array
        :param count: Length of the uniform array (default 1)
        :param uniform: For auto-injection for uniform instance. Do not use.
        """
        GL.glUniform4dv(uniform.location, count, value)

    # --- Signed Integers ---

    @uniform_type(GL.GL_INT)
    def uniform_1i(self, name, value, uniform=None):
        """
        Sets an int

        :param name: Name of the uniform
        :param value: Integer value
        :param uniform: For auto-injection for uniform instance. Do not use.
        """
        GL.glUniform1i(uniform.location, value)

    @uniform_type(GL.GL_INT_VEC2)
    def uniform_2i(self, name, x, y, uniform=None):
        """
        Sets an ivec2

        :param name: Uniform name
        :param x: Integer
        :param y: Integer
        :param uniform: For auto-injection for uniform instance. Do not use.
        """
        GL.glUniform2i(uniform.location, x, y)

    @uniform_type(GL.GL_INT_VEC3)
    def uniform_3i(self, name, x, y, z, uniform=None):
        """
        Sets an ivec3

        :param name: Uniform name
        :param x: Integer
        :param y: Integer
        :param z: Integer
        :param uniform: For auto-injection for uniform instance. Do not use.
        """
        GL.glUniform3i(uniform.location, x, y, z)

    @uniform_type(GL.GL_INT_VEC4)
    def uniform_4i(self, name, x, y, z, w, uniform=None):
        """
        Sets an ivec4

        :param name: Uniform name
        :param x: Integer
        :param y: Integer
        :param z: Integer
        :param w: Integer
        :param uniform: For auto-injection for uniform instance. Do not use.
        """
        GL.glUniform4i(uniform.location, x, y, z, w)

    # --- Signed Integers Arrays ---

    @uniform_type(GL.GL_INT)
    def uniform_1iv(self, name, value, count=1, uniform=None):
        """
        Sets an int

        :param name: Name of the uniform
        :param value: integer array
        :param count: Length of the uniform array (default 1)
        :param uniform: For auto-injection for uniform instance. Do not use.
        """
        GL.glUniform1iv(uniform.location, count, value)

    @uniform_type(GL.GL_INT_VEC2)
    def uniform_2iv(self, name, value, count=1, uniform=None):
        """
        Sets an ivec2

        :param name: Uniform name
        :param value: integer array
        :param count: Length of the uniform array (default 1)
        :param uniform: For auto-injection for uniform instance. Do not use.
        """
        GL.glUniform2iv(uniform.location, count, value)

    @uniform_type(GL.GL_INT_VEC3)
    def uniform_3iv(self, name, value, count=1, uniform=None):
        """
        Sets an ivec3

        :param name: Uniform name
        :param value: integer array
        :param count: Length of the uniform array (default 1)
        :param uniform: For auto-injection for uniform instance. Do not use.
        """
        GL.glUniform3iv(uniform.location, count, value)

    @uniform_type(GL.GL_INT_VEC4)
    def uniform_4iv(self, name, value, count=1, uniform=None):
        """
        Sets an ivec4

        :param name: Uniform name
        :param value: integer array
        :param count: Length of the uniform array (default 1)
        :param uniform: For auto-injection for uniform instance. Do not use.
        """
        GL.glUniform4iv(uniform.location, count, value)

    # --- Unsigned Integers ---

    @uniform_type(GL.GL_UNSIGNED_INT)
    def uniform_1ui(self, name, value, uniform=None):
        """
        Sets an uint

        :param name: Name of the uniform
        :param value: Integer value
        :param uniform: For auto-injection for uniform instance. Do not use.
        """
        GL.glUniform1ui(uniform.location, value)

    @uniform_type(GL.GL_UNSIGNED_INT_VEC2)
    def uniform_2ui(self, name, x, y, uniform=None):
        """
        Sets an uvec2

        :param name: Uniform name
        :param x: Integer
        :param y: Integer
        :param uniform: For auto-injection for uniform instance. Do not use.
        """
        GL.glUniform2ui(uniform.location, x, y)

    @uniform_type(GL.GL_UNSIGNED_INT_VEC3)
    def uniform_3ui(self, name, x, y, z, uniform=None):
        """
        Sets an uvec3

        :param name: Uniform name
        :param x: Integer
        :param y: Integer
        :param z: Integer
        :param uniform: For auto-injection for uniform instance. Do not use.
        """
        GL.glUniform3ui(uniform.location, x, y, z)

    @uniform_type(GL.GL_UNSIGNED_INT_VEC4)
    def uniform_4ui(self, name, x, y, z, w, uniform=None):
        """
        Sets an uvec4

        :param name: Uniform name
        :param x: Integer
        :param y: Integer
        :param z: Integer
        :param w: Integer
        :param uniform: For auto-injection for uniform instance. Do not use.
        """
        GL.glUniform4ui(uniform.location, x, y, z, w)

    # --- Unsigned Integer Arrays ---

    @uniform_type(GL.GL_UNSIGNED_INT)
    def uniform_1uiv(self, name, value, count=1, uniform=None):
        """
        Sets an uint

        :param name: Name of the uniform
        :param value: integer array
        :param count: Length of the uniform array (default 1)
        :param uniform: For auto-injection for uniform instance. Do not use.
        """
        GL.glUniform1uiv(uniform.location, count, value)

    @uniform_type(GL.GL_UNSIGNED_INT_VEC2)
    def uniform_2uiv(self, name, value, count=1, uniform=None):
        """
        Sets an uvec2

        :param name: Uniform name
        :param value: integer array
        :param count: Length of the uniform array (default 1)
        :param uniform: For auto-injection for uniform instance. Do not use.
        """
        GL.glUniform2uiv(uniform.location, count, value)

    @uniform_type(GL.GL_UNSIGNED_INT_VEC3)
    def uniform_3uiv(self, name, value, count=1, uniform=None):
        """
        Sets an uvec3

        :param name: Uniform name
        :param value: integer array
        :param count: Length of the uniform array (default 1)
        :param uniform: For auto-injection for uniform instance. Do not use.
        """
        GL.glUniform3uiv(uniform.location, count, value)

    @uniform_type(GL.GL_UNSIGNED_INT_VEC4)
    def uniform_4uiv(self, name, value, count=1, uniform=None):
        """
        Sets an uvec4

        :param name: Uniform name
        :param value: integer array
        :param count: Length of the uniform array (default 1)
        :param uniform: For auto-injection for uniform instance. Do not use.
        """
        GL.glUniform4uiv(uniform.location, count, value)

    # --- Booleans ---

    @uniform_type(GL.GL_BOOL)
    def uniform_1b(self, name, value, uniform=None):
        """
        Sets an bool

        :param name: Name of the uniform
        :param value: Integer value
        :param uniform: For auto-injection for uniform instance. Do not use.
        """
        GL.glUniform1i(uniform.location, value)

    @uniform_type(GL.GL_BOOL_VEC2)
    def uniform_2b(self, name, x, y, uniform=None):
        """
        Sets an bvec2

        :param name: Uniform name
        :param x: bool
        :param y: bool
        :param uniform: For auto-injection for uniform instance. Do not use.
        """
        GL.glUniform2i(uniform.location, x, y)

    @uniform_type(GL.GL_BOOL_VEC3)
    def uniform_3b(self, name, x, y, z, uniform=None):
        """
        Sets an bvec3

        :param name: Uniform name
        :param x: bool
        :param y: bool
        :param z: bool
        :param uniform: For auto-injection for uniform instance. Do not use.
        """
        GL.glUniform3i(uniform.location, x, y, z)

    @uniform_type(GL.GL_BOOL_VEC4)
    def uniform_4b(self, name, x, y, z, w, uniform=None):
        """
        Sets an bvec4

        :param name: Uniform name
        :param x: bool
        :param y: bool
        :param z: bool
        :param w: bool
        :param uniform: For auto-injection for uniform instance. Do not use.
        """
        GL.glUniform4i(uniform.location, x, y, z, w)

    # --- Matrices ---

    @uniform_type(GL.GL_FLOAT_MAT2)
    def uniform_mat2(self, name, mat, transpose=GL.GL_FALSE, uniform=None):
        """
        Sets a mat3 uniform

        :param name: Name of the uniform
        :param mat: matrix
        :param transpose: Traspose the matrix (true/false)
        :param uniform: For auto-injection for uniform instance. Do not use.
        """
        if mat is None:
            raise ShaderError("uniform_mat2: Attempted to set uniform to None")
        GL.glUniformMatrix2fv(uniform.location, 1, transpose, mat)

    @uniform_type(GL.GL_FLOAT_MAT3)
    def uniform_mat3(self, name, mat, transpose=GL.GL_FALSE, uniform=None):
        """
        Sets a mat3 uniform

        :param name: Name of the uniform
        :param mat: matrix
        :param transpose: Traspose the matrix (true/false)
        :param uniform: For auto-injection for uniform instance. Do not use.
        """
        if mat is None:
            raise ShaderError("uniform_mat3: Attempted to set uniform to None")
        GL.glUniformMatrix3fv(uniform.location, 1, transpose, mat)

    @uniform_type(GL.GL_FLOAT_MAT4)
    def uniform_mat4(self, name, mat, transpose=GL.GL_FALSE, uniform=None):
        """
        Set a mat4 uniform

        :param name: Name of the uniform
        :param mat: matrix
        :param transpose: Traspose the matrix (true/false)
        :param uniform: For auto-injection for uniform instance. Do not use.
        """
        if mat is None:
            raise ShaderError("uniform_mat4: Attempted to set uniform to None")
        GL.glUniformMatrix4fv(uniform.location, 1, transpose, mat)

    # --- Sampler ---

    @uniform_type(GL.GL_SAMPLER_1D, name_arg_index=2)
    def uniform_sampler_1d(self, unit, name, texture, sampler=None, uniform=None):
        """
        Sets a sampler1d

        :param unit: The texture unit to use (0 - N)
        :param name: Name of the uniform
        :param texture: The Texture object
        :param uniform: For auto-injection for uniform instance. Do not use.
        """
        GL.glActiveTexture(GL.GL_TEXTURE0 + unit)
        texture.bind()
        if sampler:
            sampler.bind(unit)
        GL.glUniform1i(uniform.location, unit)

    @uniform_type(GL.GL_SAMPLER_2D, name_arg_index=2)
    def uniform_sampler_2d(self, unit, name, texture, sampler=None, uniform=None):
        """
        Sets a sampler2d

        :param unit: The texture unit to use (0 - N)
        :param name: Name of the uniform
        :param texture: The Texture object
        :param uniform: For auto-injection for uniform instance. Do not use.
        """
        GL.glActiveTexture(GL.GL_TEXTURE0 + unit)
        texture.bind()
        if sampler:
            sampler.bind(unit)
        GL.glUniform1i(uniform.location, unit)

    @uniform_type(GL.GL_SAMPLER_3D, name_arg_index=2)
    def uniform_sampler_3d(self, unit, name, texture, sampler=None, uniform=None):
        """
        Sets a sampler3d

        :param unit: The texture unit to use (0 - N)
        :param name: Name of the uniform
        :param texture: The Texture object
        :param uniform: For auto-injection for uniform instance. Do not use.
        """
        GL.glActiveTexture(GL.GL_TEXTURE0 + unit)
        texture.bind()
        if sampler:
            sampler.bind(unit)
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
