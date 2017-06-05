from OpenGL import GL
from demosys.opengl import Texture

WINDOW_FBO = None


class WindowFBO:
    """
    Fake FBO representing default render target
    """
    def __init__(self, window):
        self.window = window

    def bind(self):
        """
        Sets the viewport back to the buffer size of the screen/window
        """
        # The expected height with the current viewport width
        expected_height = int(self.window.buffer_width / self.window.aspect_ratio)
        # How much positive or negative y padding
        blank_space = self.window.buffer_height - expected_height

        GL.glViewport(0, int(blank_space / 2),
                      self.window.buffer_width, expected_height)

    def release(self):
        """
        Dummy release method.
        """
        pass

    def clear(self):
        """
        Dummy clear method.
        """
        pass


class FBO:
    """Frame buffer object"""
    def __init__(self):
        self.color_buffers = []
        self.color_buffers_ids = []
        self.depth_buffer = None
        self.fbo = GL.glGenFramebuffers(1)

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

        push_fbo(self)
        if len(self.color_buffers) > 1:
            GL.glDrawBuffers(len(self.color_buffers), self.color_buffers_ids)

        w, h = self.size
        GL.glViewport(0, 0, w, h)

    def release(self, stack=True):
        """
        Bind FBO popping it from the stack

        :param stack: (bool) If the bind should be popped form the FBO stack.
        """
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0)
        if not stack:
            return

        parent = pop_fbo(self)
        if parent:
            parent.bind()

    def clear(self):
        """
        Clears the FBO using ``glClear``.
        """
        self.bind()
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT | GL.GL_STENCIL_BUFFER_BIT)
        self.release()

    @classmethod
    def create(cls, width, height, depth=False,
               internal_format=GL.GL_RGBA8, format=GL.GL_RGBA, type=GL.GL_UNSIGNED_BYTE, layers=1):
        """
        Convenient shortcut for creating single color attachment FBOs

        :param width: Color buffer width
        :param height: Coller buffer height
        :param depth: (bool) Create a depth attachment
        :param internal_format: The internalformat of the color buffer
        :param format: The format of the color buffer
        :param type: The type of the color buffer
        :return: A new FBO
        """
        fbo = FBO()
        fbo.bind(stack=False)

        # Add N layers of color attachments
        for layer in range(layers):
            c = Texture.create_2d(width=width, height=height, internal_format=internal_format, format=format, type=type,
                                  wrap_s=GL.GL_CLAMP_TO_EDGE, wrap_t=GL.GL_CLAMP_TO_EDGE, wrap_r=GL.GL_CLAMP_TO_EDGE)
            fbo.add_color_attachment(c)

        # Set depth attachment is specified
        if depth:
            d = Texture.create_2d(width=width, height=height,
                                  internal_format=GL.GL_DEPTH24_STENCIL8, format=GL.GL_DEPTH_COMPONENT,
                                  wrap_s=GL.GL_CLAMP_TO_EDGE, wrap_t=GL.GL_CLAMP_TO_EDGE, wrap_r=GL.GL_CLAMP_TO_EDGE)
            fbo.set_depth_attachment(d)

        fbo.check_status()
        fbo.release(stack=False)
        return fbo

    def add_color_attachment(self, texture):
        """
        Add a texture as a color attachment.

        :param texture: The Texture object
        """
        # Internal states
        self.color_buffers_ids.append(GL.GL_COLOR_ATTACHMENT0 + len(self.color_buffers))
        self.color_buffers.append(texture)

        # Make sure the FBO is bound
        self.bind(stack=False)

        # Attach to fbo
        GL.glFramebufferTexture2D(
            GL.GL_FRAMEBUFFER,
            self.color_buffers_ids[-1],
            GL.GL_TEXTURE_2D,
            self.color_buffers[-1].texture,
            0
        )
        self.release(stack=False)

    def set_depth_attachment(self, texture):
        """
        Set a texture as depth attachment.

        :param texture: The Texture object
        """
        self.depth_buffer = texture

        # Make sure the FBO is bound
        self.bind(stack=False)

        # Attach to fbo
        GL.glFramebufferTexture2D(
            GL.GL_FRAMEBUFFER,
            GL.GL_DEPTH_ATTACHMENT,
            GL.GL_TEXTURE_2D,
            self.depth_buffer.texture,
            0
        )
        self.release(stack=False)

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


# Internal FBO bind stack so we can support hierarchical binding
FBO_STACK = []


def push_fbo(fbo):
    """Push fbo into the stack"""
    global FBO_STACK
    FBO_STACK.append(fbo)
    if len(FBO_STACK) > 8:
        raise FBOError("FBO stack overflow. You probably forgot to release a bind somewhere.")


def pop_fbo(fbo):
    """
    Pops the fbo out of the stack
    Returns: The last last fbo in the stack
    """
    global FBO_STACK
    if not FBO_STACK:
        raise FBOError("FBO stack is already empty. You are probably releasing a FBO twice or forgot to bind.")
    fbo_out = FBO_STACK.pop()
    if fbo_out != fbo:
        raise FBOError("Incorrect FBO release order")
    if FBO_STACK:
        return FBO_STACK[-1]
    return WINDOW_FBO


class FBOError(Exception):
    """Generic FBO Error"""
    pass
