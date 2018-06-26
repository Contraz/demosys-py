from pyrr import matrix44
from demosys.opengl import FBO
from demosys.opengl import Texture2D, DepthTexture
from OpenGL import GL
from demosys import resources
from demosys import geometry


class PointLight:
    """A point light and its properties"""
    def __init__(self, position, radius):
        self._position = position
        self.radius = radius
        self.matrix = None

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, pos):
        self._position = pos
        self.matrix = matrix44.create_from_translation(pos)


class DeferredRenderer:

    def __init__(self, width, height, gbuffer=None, lightbuffer=None):
        self.width = width
        self.height = height
        self.size = (width, height)

        # FBOs
        self.gbuffer = gbuffer
        self.lightbuffer = lightbuffer

        # Light Info
        self.point_lights = []

        # Create geometry buffer if not supplied
        depth_buffer = DepthTexture(self.size)

        if not self.gbuffer:
            self.gbuffer = FBO.create_from_textures(
                [
                    Texture2D.create(self.size, 4, dtype='f1'),
                    Texture2D.create(self.size, 3, dtype='f2'),
                ],
                depth_buffer=depth_buffer,
            )

        if not self.lightbuffer:
            self.lightbuffer = FBO.create_from_textures(
                [Texture2D.create(self.size, 4)],
                depth_buffer=depth_buffer,
            )

        # Unit cube for point lights (cube with radius 1.0)
        self.unit_cube = geometry.cube(width=2, height=2, depth=2)
        self.point_light_shader = resources.shaders.get("deferred/light_point.glsl", create=True)

        # Debug draw lights
        self.debug_shader = resources.shaders.get("deferred/debug.glsl", create=True)

        # Combine shader
        self.combine_shader = resources.shaders.get("deferred/combine.glsl", create=True)
        self.quad = geometry.quad_fs()

    def draw_buffers(self, near, far):
        """
        Draw framebuffers for debug purposes.
        We need to supply near and far plane so the depth buffer can be linearized when visualizing.

        :param near: Projection near value
        :param far: Projection far value
        """
        self.gbuffer.draw_color_layer(layer=0, pos=(0.0, 0.0), scale=(0.25, 0.25))
        self.gbuffer.draw_color_layer(layer=1, pos=(0.5, 0.0), scale=(0.25, 0.25))
        self.gbuffer.draw_depth(near, far, pos=(1.0, 0.0), scale=(0.25, 0.25))
        self.lightbuffer.draw_color_layer(layer=0, pos=(1.5, 0.0), scale=(0.25, 0.25))

    def add_point_light(self, position, radius):
        """Add point light"""
        self.point_lights.append(PointLight(position, radius))

    def render_lights(self, camera_matrix, projection):
        """Render light volumes"""
        # Disable culling so lights can be rendered when inside volumes
        GL.glEnable(GL.GL_CULL_FACE)
        GL.glFrontFace(GL.GL_CW)
        # No depth testing
        GL.glDisable(GL.GL_DEPTH_TEST)
        # Enable additive blending
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_ONE, GL.GL_ONE)

        with self.lightbuffer:
            for light in self.point_lights:
                # Calc light properties
                light_size = light.radius
                m_light = matrix44.multiply(light.matrix, camera_matrix)
                # Draw the light volume
                self.point_light_shader.uniform("m_proj", projection.tobytes())
                self.point_light_shader.uniform("m_light", m_light.astype('f4').tobytes())
                self.gbuffer.color_buffers[1].use(location=0)
                self.point_light_shader.uniform("g_normal", 0)
                self.gbuffer.depth_buffer.use(location=1)
                self.point_light_shader.uniform("g_depth", 1)
                self.point_light_shader.uniform("screensize", (self.width, self.height))
                self.point_light_shader.uniform("proj_const", projection.projection_constants)
                self.point_light_shader.uniform("radius", light_size)
                self.unit_cube.draw(self.point_light_shader)

        GL.glDisable(GL.GL_BLEND)
        GL.glDisable(GL.GL_CULL_FACE)

    def render_lights_debug(self, camera_matrix, projection):
        """Render outlines of light volumes"""
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)

        for light in self.point_lights:
            m_mv = matrix44.multiply(light.matrix, camera_matrix)
            light_size = light.radius
            self.debug_shader.uniform("m_proj", projection.tobytes())
            self.debug_shader.uniform("m_mv", m_mv.astype('f4'))
            self.debug_shader.uniform("size", light_size)
            self.unit_cube.draw(self.debug_shader, mode=GL.GL_LINE_STRIP)

        GL.glDisable(GL.GL_BLEND)

    def render_geometry(self, cam_matrix, projection):
        raise NotImplementedError("render_geometry() not implemented")

    def combine(self):
        """Combine diffuse and light buffer"""
        self.gbuffer.color_buffers[0].use(location=0)
        self.combine_shader.uniform("diffuse_buffer", 0)
        self.lightbuffer.color_buffers[0].use(location=1)
        self.combine_shader.uniform("light_buffer", 1)
        self.quad.draw(self.combine_shader)

    def clear(self):
        """clear all buffers"""
        self.gbuffer.clear()
        self.lightbuffer.clear()
