import moderngl
from demosys import context

from .base import BaseTexture


class DepthTexture(BaseTexture):
    """
    A DepthTexture is a texture for storing depth information during rendering.
    They are attachments to :py:class:`demosys.opengl.FBO`.
    """

    # Class attributes for drawing the texture
    quad = None
    shader = None
    sampler = None

    def __init__(self, size, data=None, samples=0, alignment=4):
        """
        Create a depth texture

        :param size: (tuple) The width and height of the texture.
        :param data: (bytes) Content of the texture.
        :param samples: The number of samples. Value 0 means no multisample format.
        :param alignment: The byte alignment 1, 2, 4 or 8.
        """
        super().__init__()
        self.mglo = self.ctx.depth_texture(size, data=data, samples=samples, alignment=alignment)
        self.mglo.filter = moderngl.LINEAR, moderngl.LINEAR
        _init_depth_texture_draw()

    @classmethod
    def create(cls, size, data=None, samples=0, alignment=4) -> 'DepthTexture':
        """
        Creates a :py:class:`DepthTexture` object

        :param size: (tuple) The width and height of the texture.
        :param data: (bytes) Content of the texture.
        :param samples: The number of samples. Value 0 means no multisample format.
        :param alignment: The byte alignment 1, 2, 4 or 8.
        :return: :py:class:`DepthTexture` object
        """
        return cls(size, data=data, samples=samples, alignment=alignment)

    def draw(self, near, far, pos=(0.0, 0.0), scale=(1.0, 1.0)):
        """
        Draw depth buffer linearized.
        By default this will draw the texture as a full screen quad.
        A sampler will be used to ensure the right conditions to draw the depth buffer.

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

        self.sampler.clear(location=0)

    @property
    def compare_func(self) -> str:
        """tuple: The compare function of the depth texture"""
        return self.mglo.compare_func

    @compare_func.setter
    def compare_func(self, value):
        self.mglo.compare_func = value


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

    DepthTexture.sampler = context.ctx().sampler(
        filter=(moderngl.LINEAR, moderngl.LINEAR),
        compare_func='',
    )
    DepthTexture.shader = program
