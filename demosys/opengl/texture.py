from typing import Tuple

from PIL import Image

import moderngl as mgl
from demosys import context
from demosys.opengl import samplers


class BaseTexture:
    """
    Wraps the basic functionality of the ModernGL methods
    """
    def __init__(self):
        self.mglo = None
        self._ctx = context.ctx()

    def use(self, location=0):
        """
        Bind the texture.

        :param location: The texture location. (GL_TEXTURE0 + location)
        """
        self.mglo.use(location)

    @property
    def ctx(self) -> mgl.Context:
        """ModernGL context"""
        return self._ctx

    @property
    def size(self) -> Tuple:
        """The size of the texture"""
        return self.mglo.size

    @property
    def width(self) -> int:
        """Width of the texture"""
        return self.mglo.width

    @property
    def height(self) -> int:
        """Height of the texture"""
        return self.mglo.height

    @property
    def dtype(self) -> str:
        """The data type of the texture"""
        return self.mglo.dtype

    @property
    def depth(self) -> bool:
        """Is this a depth texture?"""
        return self.mglo.depth

    @property
    def swizzle(self):
        return self.mglo.swizzle

    def build_mipmaps(self, base=0, max_level=1000):
        """
        Build mipmaps for this texture

        :param base: Level to build from
        :param max_level: Max levels
        """
        self.mglo.build_mipmaps(base=base, max_level=max_level)

    def read(self, level: int=0, alignment: int=1) -> bytes:
        """
        Read the content of the texture into a buffer.

        :param level: The mipmap level.
        :param alignment: The byte alignment of the pixels.
        :return: bytes
        """
        return self.mglo.read(level=level, alignment=alignment)

    def read_into(self, buffer: bytearray, level: int=0, alignment: int=1, write_offset: int=0):
        """
        Read the content of the texture into a buffer.

        :param buffer: (bytearray) The buffer that will receive the pixels.
        :param level: (int) The mipmap level.
        :param alignment: (int) The byte alignment of the pixels.
        :param write_offset: (int) The write offset.
        """
        self.mglo.read_into(buffer, level=level, alignment=alignment, write_offset=write_offset)

    def write(self, data: bytes, viewport=None, level: int=0, alignment: int=1):
        """
        Update the content of the texture.

        :param data: (bytes) – The pixel data.
        :param viewport: (tuple) – The viewport.
        :param level: (int) – The mipmap level.
        :param alignment: (int) – The byte alignment of the pixels.
        """
        self.mglo.write(data, viewport=viewport, level=level, alignment=alignment)


class Texture2D(BaseTexture):
    """2D Texture"""

    # Class attributes for drawing the texture
    quad = None
    shader = None

    def __init__(self, path: str=None, mipmap: bool=False, **kwargs):
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
    def create(cls, size, components=4, data=None, samples=0, alignment=1, dtype='f1', mipmap=False) -> 'Texture2D':
        """
        Creates a 2d texture.
        All parameters are passed on the texture initializer.

        :param size: (tuple) Width and height of the texture
        :param components: Number of components
        :param data: Buffer data for the texture
        :param samples: Number of samples when using multisaple texture
        :param alignment: Data alignment (1, 2, 4 or 8)
        :param dtype: Datatype for each component
        :param mipmap: Generate mipmaps
        :return: Texture object
        """
        texture = Texture2D(path="dynamic", mipmap=mipmap)

        texture.mglo = texture.ctx.texture(
            size,
            components,
            data=data,
            samples=samples,
            alignment=alignment,
            dtype=dtype,
        )

        if mipmap:
            texture.build_mipmaps()

        return texture

    @classmethod
    def from_image(cls, path, image=None, **kwargs):
        """
        Creates a texture from a image file using Pillow/PIL.
        Additional parameters is passed to the texture initializer.

        :param path: The path to the file
        :param image: The PIL/Pillow image object (Can be None)
        :return: Texture object
        """
        texture = Texture2D(path=path, **kwargs)
        if image:
            texture.set_image(image)
        return texture

    def set_image(self, image, flip=True):
        """
        Set pixel data using a image file with PIL/Pillow.

        :param image: The PIL/Pillow image object
        :param flip: Flip the image top to bottom
        """
        if flip:
            image = image.transpose(Image.FLIP_TOP_BOTTOM)

        self.mglo = self.ctx.texture(
            image.size,
            4,
            image.convert("RGBA").tobytes(),
        )

        if self.mipmap:
            self.build_mipmaps()

    def draw(self, pos=(0.0, 0.0), scale=(1.0, 1.0)):
        """
        Draw texture

        :param pos: (tuple) offset x, y
        :param scale: (tuple) scale x, y
        """
        self.shader.uniform("offset", (pos[0] - 1.0, pos[1] - 1.0))
        self.shader.uniform("scale", (scale[0], scale[1]))
        self.use(location=0)
        self.shader.uniform("texture0", 0)
        self.quad.draw(self.shader)


class TextureArray(BaseTexture):

    def __init__(self, path: str=None, mipmap: bool=False, layers=0, **kwargs):
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
        self.layers = layers
        self.mipmap = mipmap

        if self.layers <= 0:
            raise ValueError("Texture {} requires a layer parameter > 0".formats(self.path))

    @classmethod
    def create(cls, size, components=4, data=None, alignment=1, dtype='f1', mipmap=False):
        """
        :param size: (x, y, layers) size and layers of the texture
        :param components: The number of components 1, 2, 3 or 4
        :param data: (bytes) Content of the texture
        :param alignment: The byte alignment 1, 2, 4 or 8
        :param dtype: (str) The data type
        :param mipmap: (bool) Generate mipmaps
        """
        texture = cls("create", mipmap=False, layers=size[2])
        texture.mglo = context.ctx().texture_array(
            size, components,
            data=data, alignment=alignment, dtype=dtype,
        )

        if mipmap:
            texture.build_mipmaps()

        return texture

    def set_image(self, image, flip=True):
        """
        Set pixel data using a image file with PIL/Pillow.

        :param image: The PIL/Pillow image object
        :param flip: Flip the image top to bottom
        """
        if flip:
            image = image.transpose(Image.FLIP_TOP_BOTTOM)

        width, height, depth = image.size[0], image.size[1] // self.layers, self.layers
        print(width, height, depth)

        self.mglo = self.ctx.texture_array(
            (width, height, depth),
            4,
            image.convert("RGBA").tobytes(),
        )

        if self.mipmap:
            self.build_mipmaps()


class DepthTexture(BaseTexture):
    """Depth Texture"""

    # Class attributes for drawing the texture
    quad = None
    shader = None
    sampler = None

    def __init__(self, size, data=None, samples=0, alignment=8):
        """
        Create a depth texture

        :param size: (tuple) The width and height of the texture.
        :param data: (bytes) Content of the texture.
        :param samples: The number of samples. Value 0 means no multisample format.
        :param alignment: The byte alignment 1, 2, 4 or 8.
        """
        super().__init__()
        self.mglo = self.ctx.depth_texture(size, data=data, samples=samples, alignment=alignment)
        self.mglo.filter = mgl.LINEAR, mgl.LINEAR
        _init_depth_texture_draw()

    @classmethod
    def create(cls, size, data=None, samples=0, alignment=8):
        return cls(size, data=data, samples=samples, alignment=alignment)

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
        self.sampler.use(location=0)
        self.use(location=0)
        self.shader.uniform("texture0", 0)

        self.quad.draw(self.shader)
        self.sampler.release()


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
        "    float z = texture(texture0, uv).r;"
        "    float d = (2.0 * near) / (far + near - z * (far - near));"
        "    out_color = vec4(d);",
        "}",
        "#endif",
    ]
    program = ShaderProgram(name="depth_shader")
    program.set_source("\n".join(src))
    program.prepare()

    DepthTexture.sampler = samplers.create(
        min_filter=mgl.LINEAR,
        mag_filter=mgl.LINEAR,
        texture_compare_mode=False,
    )
    DepthTexture.shader = program
