from PIL import Image

import moderngl
from demosys import context

from .base import BaseTexture, image_data


class Texture2D(BaseTexture):
    """
    A Texture is an OpenGL object that contains one or more images that all
    have the same image format. A texture can be used in two ways. It can
    be the source of a texture access from a Shader, or it can be used
    as a render target.
    """

    # Class attributes for drawing the texture
    quad = None
    shader = None
    sampler = None

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
        :return: :py:class:`Texture2D` object
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
        :return: :py:class:`Texture2D` object
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

        components, data = image_data(image)

        self.mglo = self.ctx.texture(
            image.size,
            components,
            data,
        )

        if self.mipmap:
            self.build_mipmaps()

    def draw(self, pos=(0.0, 0.0), scale=(1.0, 1.0)):
        """
        Draw texture using a fullscreen quad.
        By default this will conver the entire screen.

        :param pos: (tuple) offset x, y
        :param scale: (tuple) scale x, y
        """
        self.shader.uniform("offset", (pos[0] - 1.0, pos[1] - 1.0))
        self.shader.uniform("scale", (scale[0], scale[1]))
        self.use(location=0)
        self.sampler.use(location=0)
        self.shader.uniform("texture0", 0)
        self.quad.draw(self.shader)
        self.sampler.clear(location=0)


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

    Texture2D.sampler = context.ctx().sampler(
        filter=(moderngl.LINEAR, moderngl.LINEAR),
    )

    Texture2D.shader = program
