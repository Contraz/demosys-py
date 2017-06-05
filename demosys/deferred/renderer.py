from demosys.opengl import FBO
from demosys.opengl import Texture
from OpenGL import GL


class DeferredRenderer:

    def __init__(self, width, height, gbuffer=None, lightbuffer=None):
        self.gbuffer = gbuffer
        self.lightbuffer = lightbuffer

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
                Texture.create_2d(width=width, height=height,
                                  internal_format=GL.GL_RED, format=GL.GL_RED, type=GL.GL_UNSIGNED_BYTE,
                                  min_filter=GL.GL_NEAREST, mag_filter=GL.GL_NEAREST,
                                  wrap_s=GL.GL_CLAMP_TO_EDGE, wrap_t=GL.GL_CLAMP_TO_EDGE)
            )
            # Attach the same depth buffer as the geometry buffer
            self.lightbuffer.set_depth_attachment(self.gbuffer.depth_buffer)

    def render_geometry(self):
        pass
