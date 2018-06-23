from OpenGL import GL
from demosys.opengl import Texture
from demosys import context

WINDOW_FBO = None


class WindowFBO:
    """Fake FBO representing default render target"""
    def __init__(self, window):
        self.window = window

    def bind(self):
        """Sets the viewport back to the buffer size of the screen/window"""
        # The expected height with the current viewport width
        expected_height = int(self.window.buffer_width / self.window.aspect_ratio)
        # How much positive or negative y padding
        blank_space = self.window.buffer_height - expected_height

        GL.glViewport(0, int(blank_space / 2),
                      self.window.buffer_width, expected_height)

    def release(self):
        """Dummy release method"""
        pass

    def clear(self):
        """Dummy clear method"""
        pass


class FBO:
    """Frame buffer object"""
    stack = []

    def __init__(self):
        self.color_buffers = []
        self.color_buffers_ids = []
        self.depth_buffer = None
        self.fbo = None

    @classmethod
    def create(cls, width, height, depth=False,
               internal_format=GL.GL_RGBA8, format=GL.GL_RGBA, type=GL.GL_UNSIGNED_BYTE, layers=1):
        """
        Create a single or multi layer FBO

        :param width: buffer width
        :param height: buffer height
        :param depth: (bool) Create a depth attachment
        :param internal_format: The internalformat of the color buffer
        :param format: The format of the color buffer
        :param type: The type of the color buffer

        :return: A new FBO
        """
        fbo = FBO()

        # Add N layers of color attachments
        for layer in range(layers):
            c = Texture.create_2d(width=width, height=height, internal_format=internal_format, format=format, type=type,
                                  wrap_s=GL.GL_CLAMP_TO_EDGE, wrap_t=GL.GL_CLAMP_TO_EDGE, wrap_r=GL.GL_CLAMP_TO_EDGE)
            fbo.color_buffers.append(c)
            fbo.color_buffers_ids.append()

        # Set depth attachment is specified
        if depth:
            d = Texture.create_2d(width=width, height=height,
                                  internal_format=GL.GL_DEPTH24_STENCIL8, format=GL.GL_DEPTH_COMPONENT,
                                  wrap_s=GL.GL_CLAMP_TO_EDGE, wrap_t=GL.GL_CLAMP_TO_EDGE, wrap_r=GL.GL_CLAMP_TO_EDGE)
            fbo.depth_buffer = d

        fbo.fbo = context.ctx().framebuffer(fbo.color_buffers, fbo.depth_buffer)

        return fbo

    @property
    def size(self):
        """
        Attempts to determine the pixel size of the FBO.
        Currently returns the size of the first color attachment.
        If the FBO has no color attachments, the depth attachment will be used.
        Raises ```FBOError`` if the size cannot be determined.

        :return: (w, h) tuple representing the size in pixels
        """
        # FIXME: How do we deal with attachments of different sizes?
        if self.color_buffers:
            return self.color_buffers[0].size

        if self.depth_buffer:
            return self.depth_buffer.size

        raise FBOError("Cannot determine size of FBO. No attachments.")

    def __enter__(self):
        """
        Entering context manager.
        This will bind the FBO and return itself.
        """
        self.bind()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit context manager.
        This will release the FBO.
        """
        self.release()

    def bind(self, stack=True):
        """
        Bind FBO adding it to the stack.

        :param stack: (bool) If the bind should push the current FBO on the stack.
        """
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, self.fbo)
        if not stack:
            return

        FBO.stack.append(self)
        if len(FBO.stack) > 8:
            raise FBOError("FBO stack overflow. You probably forgot to release a bind somewhere.")

        # if len(self.color_buffers) > 1:
        #     GL.glDrawBuffers(len(self.color_buffers), self.color_buffers_ids)

        self.fbo.use()

        # w, h = self.size
        # GL.glViewport(0, 0, w, h)

    def release(self, stack=True):
        """
        Bind FBO popping it from the stack

        :param stack: (bool) If the bind should be popped form the FBO stack.
        """
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0)
        if not stack:
            return

        # Are we trying to release an FBO that is not bound?
        if not FBO.stack:
            raise FBOError("FBO stack is already empty. You are probably releasing a FBO twice or forgot to bind.")
        fbo_out = FBO.stack.pop()

        # Make sure we released this FBO and not some other random one
        if fbo_out != self:
            raise FBOError("Incorrect FBO release order")

        # Find the parent fbo
        if FBO.stack:
            parent = FBO.stack[-1]
        else:
            parent = WINDOW_FBO

        # Bind the parent FBO
        if parent:
            parent.bind()

    def clear(self):
        """
        Clears the FBO using ``glClear``.
        """
        self.fbo.clear()
        # self.bind()
        # GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT | GL.GL_STENCIL_BUFFER_BIT)
        # self.release()

    def draw_color_layer(self, layer=0, pos=(0.0, 0.0), scale=(1.0, 1.0)):
        """
        Draw a color layer in the FBO.
        :param layer: Layer ID
        :param pos: (tuple) offset x, y
        :param scale: (tuple) scale x, y
        """
        self.color_buffers[layer].draw(pos=pos, scale=scale)

    def check_status(self):
        """
        Checks the completeness of the FBO
        """
        status = GL.glCheckFramebufferStatus(GL.GL_FRAMEBUFFER)
        incomplete_states = {
            GL.GL_FRAMEBUFFER_UNSUPPORTED: "Framebuffer unsupported. Try another format.",
            GL.GL_FRAMEBUFFER_INCOMPLETE_ATTACHMENT: "Framebuffer incomplete attachment",
            GL.GL_FRAMEBUFFER_INCOMPLETE_MISSING_ATTACHMENT: "Framebuffer missing attachment",
            GL.GL_FRAMEBUFFER_INCOMPLETE_DIMENSIONS: "Framebuffer unsupported dimension.",
            GL.GL_FRAMEBUFFER_INCOMPLETE_FORMATS: "Framebuffer incoplete formats.",
            GL.GL_FRAMEBUFFER_INCOMPLETE_DRAW_BUFFER: "Framebuffer incomplete draw buffer.",
            GL.GL_FRAMEBUFFER_INCOMPLETE_READ_BUFFER: "Framebuffer incomplete read buffer",
        }
        if status == GL.GL_FRAMEBUFFER_COMPLETE:
            return
        s = incomplete_states.get(status, "Unknown error")
        raise FBOError(s)

    def __repr__(self):
        return "<FBO {} color_attachments={} depth_attachement={}".format(
            self.fbo,
            self.color_buffers,
            self.depth_buffer,
        )


class FBOError(Exception):
    """Generic FBO Error"""
    pass
