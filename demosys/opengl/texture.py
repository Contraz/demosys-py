from typing import Tuple
from PIL import Image
from demosys import context


class BaseTexture:
    """
    Wraps the basic functionality of the ModernGL methods
    """

    def __init__(self):
        self._texture = None

    def use(self, location=0):
        """
        Bind the texture.

        :param location: The texture location. (GL_TEXTURE0 + location)
        """
        self._texture.use(location)

    @property
    def size(self) -> Tuple:
        """The size of the texture"""
        return self._texture.size

    @property
    def width(self) -> int:
        """Width of the texture"""
        return self._texture.width

    @property
    def height(self) -> int:
        """Height of the texture"""
        return self._texture.height

    @property
    def dtype(self) -> str:
        """The data type of the texture"""
        return self._texture.dtype

    @property
    def depth(self) -> bool:
        """Is this a depth texture?"""
        return self.depth

    @property
    def mgl_instance(self):
        return self._texture

    def read(self, level: int=0, alignment: int=1) -> bytes:
        """
        Read the content of the texture into a buffer.

        :param level: The mipmap level.
        :param alignment: The byte alignment of the pixels.
        :return: bytes
        """
        return self._texture.read(level=level, alignment=alignment)

    def read_into(self, buffer: bytearray, level: int=0, alignment: int=1, write_offset: int=0):
        """
        Read the content of the texture into a buffer.

        :param buffer: (bytearray) The buffer that will receive the pixels.
        :param level: (int) The mipmap level.
        :param alignment: (int) The byte alignment of the pixels.
        :param write_offset: (int) The write offset.
        """
        self._texture.read_into(buffer, level=level, alignment=alignment, write_offset=write_offset)

    def write(self, data: bytes, viewport=None, level: int=0, alignment: int=1):
        """
        Update the content of the texture.

        :param data: (bytes) – The pixel data.
        :param viewport: (tuple) – The viewport.
        :param level: (int) – The mipmap level.
        :param alignment: (int) – The byte alignment of the pixels.
        """
        self._texture.write(data, viewport=viewport, level=level, alignment=alignment)


class Texture2D(BaseTexture):
    """2D Texture"""

    # Class attributes for drawing the texture
    quad = None
    shader = None

    def __init__(self, path: str=None, mipmap: bool=False):
        """
        Initialize configuration for this texture.
        This doesn't create the OpenGL texture objects itself
        and is mostly used by the resource loading system.

        :param path: The global resource path for the texture to load
        :param mipmap: (bool) Should we generate mipmaps?
        """
        super().__init__()
        # Info for resource loader
        self.path = path
        self.mipmap = mipmap

        _init_texture2d_draw()

    @classmethod
    def create(cls, size, components, data=None, samples=0, alignment=1, dtype='f1', mipmap=False) -> 'Texture2D':
        """
        Creates a 2d texture.
        All parameters are passed on the texture initializer.

        :return: Texture object
        """
        t = Texture2D(path="dynamic", mipmap=mipmap)

        t._texture = context.ctx().texture(
            size,
            components,
            data=data,
            samples=samples,
            alignment=alignment,
            dtype=dtype,
        )

        if mipmap:
            t._texture.build_mipmaps()

        return t

    @classmethod
    def from_image(cls, path, image=None, **kwargs):
        """
        Creates a texture from a image file using Pillow/PIL.
        Additional parameters is passed to the texture initializer.

        :param path: The path to the file
        :param image: The PIL/Pillow image object (Can be None)
        :return: Texture object
        """
        t = Texture2D(path=path, **kwargs)
        if image:
            t.set_image(image)
        return t

    def set_image(self, image, flip=True):
        """
        Set pixel data using a image file with PIL/Pillow.

        :param image: The PIL/Pillow image object
        :param flip: Flip the image top to bottom
        """
        if flip:
            image = image.transpose(Image.FLIP_TOP_BOTTOM)

        self._texture = context.ctx().texture(
            image.size,
            4,
            image.convert("RGBA").tobytes(),
        )

        if self.mipmap:
            self._texture.build_mipmaps()

    def draw(self, pos=(0.0, 0.0), scale=(1.0, 1.0)):
        """
        Draw texture
        :param shader: override shader
        :param pos: (tuple) offset x, y
        :param scale: (tuple) scale x, y
        """
        self.shader.uniform("offset", (pos[0] - 1.0, pos[1] - 1.0))
        self.shader.uniform("scale", (scale[0], scale[1]))
        self.use(location=0)
        self.shader.uniform("texture0", 0)
        self.quad.draw(self.shader)


class DepthTexture(BaseTexture):
    """Depth Texture"""

    # Class attributes for drawing the texture
    quad = None
    shader = None

    def __init__(self, size, data=None, samples=0, alignment=4):
        """
        Create a depth texture

        :param size: (tuple) The width and height of the texture.
        :param data: (bytes) Content of the texture.
        :param samples: The number of samples. Value 0 means no multisample format.
        :param alignment: The byte alignment 1, 2, 4 or 8.
        """
        super().__init__()
        self._texture = context.ctx().depth_texture(size, data=data, samples=samples, alignment=alignment)
        _init_depth_texture_draw()

    def draw(self, near, far, pos=(0.0, 0.0), scale=(1.0, 1.0)):
        """
        Draw depth buffer linearized.
        :param near: Near plane in projection
        :param far: Far plane in projection
        :param pos: (tuple) offset x, y
        :param scale: (tuple) scale x, y
        """
        self.shader.uniform("offset", (pos[0] - 1.0, pos[1] - 1.0))
        self.shader.uniform("scale", (scale[0], scale[1]))
        self.shader.uniform("near", near)
        self.shader.uniform("far", far)
        self._texture.use(location=0)
        self.shader.uniform("texture0", 0)

        self.quad.draw(self.shader)


def _init_texture2d_draw():
    """Initialize geometry and shader for drawing FBO layers"""
    from demosys.opengl import ShaderProgram
    from demosys import geometry

    if Texture2D.quad:
        return

    Texture2D.quad = geometry.quad_fs()
    # Shader for drawing color layers
    src = [
        "#version 330",
        "#if defined VERTEX_SHADER",
        "in vec3 in_position;",
        "in vec2 in_uv;",
        "out vec2 uv;",
        "uniform vec2 offset;",
        "uniform vec2 scale;",
        "",
        "void main() {",
        "    uv = in_uv;"
        "    gl_Position = vec4((in_position.xy + vec2(1.0, 1.0)) * scale + offset, 0.0, 1.0);",
        "}",
        "",
        "#elif defined FRAGMENT_SHADER",
        "out vec4 out_color;",
        "in vec2 uv;",
        "uniform sampler2D texture0;",
        "void main() {",
        "    out_color = texture(texture0, uv);",
        "}",
        "#endif",
    ]
    program = ShaderProgram(name="fbo_shader")
    program.set_source("\n".join(src))
    program.prepare()

    Texture2D.shader = program


def _init_depth_texture_draw():
    """Initialize geometry and shader for drawing FBO layers"""
    from demosys.opengl import ShaderProgram
    from demosys import geometry

    if DepthTexture.quad:
        return

    DepthTexture.quad = geometry.quad_fs()
    # Shader for drawing depth layers
    src = [
        "#version 330",
        "#if defined VERTEX_SHADER",
        "in vec3 in_position;",
        "in vec2 in_uv;",
        "out vec2 uv;",
        "uniform vec2 offset;",
        "uniform vec2 scale;",
        "",
        "void main() {",
        "    uv = in_uv;"
        "    gl_Position = vec4((in_position.xy + vec2(1.0, 1.0)) * scale + offset, 0.0, 1.0);",
        "}",
        "",
        "#elif defined FRAGMENT_SHADER",
        "out vec4 out_color;",
        "in vec2 uv;",
        "uniform sampler2D texture0;",
        "uniform float near;"
        "uniform float far;"
        "void main() {",
        "    float z = texture(texture0, uv).x;"
        "    float d = (2.0 * near) / (far + near - z * (far - near));"
        "    out_color = vec4(d);",
        "}",
        "#endif",
    ]
    program = ShaderProgram(name="depth_shader")
    program.set_source("\n".join(src))
    program.prepare()

    DepthTexture.shader = program
