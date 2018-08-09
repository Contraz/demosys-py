from pyrr import matrix44

import moderngl
from demosys import context, geometry, resources
from demosys.opengl import texture


class PointLight:
    """A point light and its properties"""
    def __init__(self, position, radius):
        self.matrix = None
        self._position = position
        self.position = position
        self.radius = radius

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

        depth_texture = self.ctx.depth_texture(self.size)

        if not self.gbuffer:
            self.gbuffer = self.ctx.framebuffer(
                (
                    self.ctx.texture(self.size, 4, dtype='f1'),
                    self.ctx.texture(self.size, 3, dtype='f2'),
                ),
                depth_attachment=depth_texture,
            )

        self.gbuffer_scope = self.ctx.scope(
            self.gbuffer,
            enable_only=moderngl.DEPTH_TEST | moderngl.CULL_FACE
        )

        if not self.lightbuffer:
            self.lightbuffer = self.ctx.framebuffer(
                self.ctx.texture(self.size, 4),
            )

        self.lightbuffer_scope = self.ctx.scope(
            self.lightbuffer,
            enable_only=moderngl.BLEND | moderngl.CULL_FACE
        )

        # Unit cube for point lights (cube with radius 1.0)
        self.unit_cube = geometry.cube(width=2, height=2, depth=2)
        self.point_light_shader = resources.programs.get("deferred/light_point.glsl", create=True)

        # Debug draw lights
        self.debug_shader = resources.programs.get("deferred/debug.glsl", create=True)

        # Combine shader
        self.combine_shader = resources.programs.get("deferred/combine.glsl", create=True)
        self.quad = geometry.quad_fs()

    @property
    def ctx(self):
        return context.ctx()

    def draw_buffers(self, near, far):
        """
        Draw framebuffers for debug purposes.
        We need to supply near and far plane so the depth buffer can be linearized when visualizing.

        :param near: Projection near value
        :param far: Projection far value
        """
        self.ctx.disable(moderngl.DEPTH_TEST)

        texture.draw(self.gbuffer.color_attachments[0], pos=(0.0, 0.0), scale=(0.25, 0.25))
        texture.draw(self.gbuffer.color_attachments[1], pos=(0.5, 0.0), scale=(0.25, 0.25))
        texture.draw_depth(self.gbuffer.depth_attachment, near, far, pos=(1.0, 0.0), scale=(0.25, 0.25))
        texture.draw(self.lightbuffer.color_attachments[0], pos=(1.5, 0.0), scale=(0.25, 0.25))

    def add_point_light(self, position, radius):
        """Add point light"""
        self.point_lights.append(PointLight(position, radius))

    def render_lights(self, camera_matrix, projection):
        """Render light volumes"""
        # Draw light volumes from the inside
        self.ctx.front_face = 'cw'
        self.ctx.blend_func = moderngl.ONE, moderngl.ONE

        texture._depth_sampler.use(location=1)
        with self.lightbuffer_scope:
            for light in self.point_lights:
                # Calc light properties
                light_size = light.radius
                m_light = matrix44.multiply(light.matrix, camera_matrix)
                # Draw the light volume
                self.point_light_shader.uniform("m_proj", projection.tobytes())
                self.point_light_shader.uniform("m_light", m_light.astype('f4').tobytes())
                self.gbuffer.color_attachments[1].use(location=0)
                self.point_light_shader.uniform("g_normal", 0)
                self.gbuffer.depth_attachment.use(location=1)
                self.point_light_shader.uniform("g_depth", 1)
                self.point_light_shader.uniform("screensize", (self.width, self.height))
                self.point_light_shader.uniform("proj_const", projection.projection_constants)
                self.point_light_shader.uniform("radius", light_size)
                self.unit_cube.draw(self.point_light_shader)

        texture._depth_sampler.clear(location=1)

    def render_lights_debug(self, camera_matrix, projection):
        """Render outlines of light volumes"""
        self.ctx.enable(moderngl.BLEND)
        self.ctx.blend_func = moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA

        for light in self.point_lights:
            m_mv = matrix44.multiply(light.matrix, camera_matrix)
            light_size = light.radius
            self.debug_shader.uniform("m_proj", projection.tobytes())
            self.debug_shader.uniform("m_mv", m_mv.astype('f4').tobytes())
            self.debug_shader.uniform("size", light_size)
            self.unit_cube.draw(self.debug_shader, mode=moderngl.LINE_STRIP)

        self.ctx.disable(moderngl.BLEND)

    def render_geometry(self, cam_matrix, projection):
        raise NotImplementedError("render_geometry() not implemented")

    def combine(self):
        """Combine diffuse and light buffer"""
        self.gbuffer.color_attachments[0].use(location=0)
        self.combine_shader.uniform("diffuse_buffer", 0)
        self.lightbuffer.color_attachments[0].use(location=1)
        self.combine_shader.uniform("light_buffer", 1)
        self.quad.draw(self.combine_shader)

    def clear(self):
        """clear all buffers"""
        self.gbuffer.clear()
        self.lightbuffer.clear()
