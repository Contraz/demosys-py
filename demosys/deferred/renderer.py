from pyrr import matrix44
from demosys.opengl import FBO
from demosys.opengl import Texture
from OpenGL import GL
from demosys import resources
from demosys.opengl import geometry


class PointLight:
    """A point light and its properties"""
    def __init__(self, position, radius):
        self.position = position
        self.radius = radius
        self.matrix = matrix44.create_from_translation(position)


class DeferredRenderer:

    def __init__(self, width, height, gbuffer=None, lightbuffer=None):
        self.width = width
        self.height = height
        # FBOs
        self.gbuffer = gbuffer
        self.lightbuffer = lightbuffer
        # Light Info
        self.point_lights = []

        # FIXME: We might want double buffering here as well
        # Create geometry buffer if not supplied
        if not self.gbuffer:
            self.gbuffer = FBO()
            # RGBA color attachment
            self.gbuffer.add_color_attachment(
                Texture.create_2d(width=width, height=height,
                                  internal_format=GL.GL_RGBA8, format=GL.GL_RGBA,
                                  min_filter=GL.GL_NEAREST, mag_filter=GL.GL_NEAREST,
                                  wrap_s=GL.GL_CLAMP_TO_EDGE, wrap_t=GL.GL_CLAMP_TO_EDGE)
            )
            # 16 bit RGB float buffer for normals
            self.gbuffer.add_color_attachment(
                Texture.create_2d(width=width, height=height,
                                  format=GL.GL_RGB, internal_format=GL.GL_RGB16F, type=GL.GL_FLOAT,
                                  min_filter=GL.GL_NEAREST, mag_filter=GL.GL_NEAREST,
                                  wrap_s=GL.GL_CLAMP_TO_EDGE, wrap_t=GL.GL_CLAMP_TO_EDGE)
            )
            # 24 bit depth, 8 bit stencil
            self.gbuffer.set_depth_attachment(
                Texture.create_2d(width=width, height=height,
                                  internal_format=GL.GL_DEPTH24_STENCIL8, format=GL.GL_DEPTH_COMPONENT,
                                  min_filter=GL.GL_NEAREST, mag_filter=GL.GL_NEAREST,
                                  wrap_s=GL.GL_CLAMP_TO_EDGE, wrap_t=GL.GL_CLAMP_TO_EDGE, wrap_r=GL.GL_CLAMP_TO_EDGE)
            )
        if not self.lightbuffer:
            self.lightbuffer = FBO()
            # 8 bit light accumulation buffer
            self.lightbuffer.add_color_attachment(
                # Texture.create_2d(width=width, height=height,
                #                   internal_format=GL.GL_RED, format=GL.GL_RED, type=GL.GL_UNSIGNED_BYTE,
                #                   min_filter=GL.GL_NEAREST, mag_filter=GL.GL_NEAREST,
                #                   wrap_s=GL.GL_CLAMP_TO_EDGE, wrap_t=GL.GL_CLAMP_TO_EDGE)
                Texture.create_2d(width=width, height=height,
                                  internal_format=GL.GL_RGBA8, format=GL.GL_RGBA,
                                  min_filter=GL.GL_NEAREST, mag_filter=GL.GL_NEAREST,
                                  wrap_s=GL.GL_CLAMP_TO_EDGE, wrap_t=GL.GL_CLAMP_TO_EDGE)
            )
            # Attach the same depth buffer as the geometry buffer
            self.lightbuffer.set_depth_attachment(self.gbuffer.depth_buffer)

        # Unit cube for point lights
        self.unit_cube = geometry.cube(width=1, height=1, depth=1)
        self.point_light_shader = resources.shaders.get("deferred/light_point.glsl", create=True)

        # Debug draw lights
        self.debug_shader = resources.shaders.get("deferred/debug.glsl", create=True)

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
        GL.glDisable(GL.GL_CULL_FACE)
        GL.glDisable(GL.GL_DEPTH_TEST)

        with self.lightbuffer:
            for light in self.point_lights:
                # Calc light properties
                light_size = light.radius * 2.0
                m_light = matrix44.multiply(light.matrix, camera_matrix)
                # Draw the light volume
                with self.unit_cube.bind(self.point_light_shader) as s:
                    s.uniform_mat4("m_proj", projection.matrix)
                    s.uniform_mat4("m_light", m_light)
                    s.uniform_sampler_2d(0, "g_normal", self.gbuffer.color_buffers[1])
                    s.uniform_sampler_2d(0, "g_depth", self.gbuffer.depth_buffer)
                    s.uniform_2f("screensize", self.width, self.height)
                    s.uniform_2f("proj_const", *projection.projection_constants)
                    s.uniform_1f("radius", light_size)
                self.unit_cube.draw()

    def render_lights_debug(self, camera_matrix, projection):
        """Render outlines of light volumes"""
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)

        for light in self.point_lights:
            m_mv = matrix44.multiply(light.matrix, camera_matrix)
            light_size = light.radius * 2
            with self.unit_cube.bind(self.debug_shader) as s:
                s.uniform_mat4("m_proj", projection.matrix)
                s.uniform_mat4("m_mv", m_mv)
                s.uniform_1f("size", light_size)
            self.unit_cube.draw(GL.GL_LINE_STRIP)

        GL.glDisable(GL.GL_BLEND)

    def render_geometry(self, cam_matrix, projection):
        raise NotImplementedError("render_geometry() not implemented")

    def clear(self):
        """clear all buffers"""
        self.gbuffer.clear()
        self.lightbuffer.clear()
