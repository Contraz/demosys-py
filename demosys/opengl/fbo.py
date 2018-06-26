from typing import List
from OpenGL import GL
from demosys.opengl import Texture2D, DepthTexture
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
        self.depth_buffer = None
        self.fbo = None

    @staticmethod
    def create_from_textures(color_buffers: List[Texture2D], depth_buffer: DepthTexture=None):
        """
        Create FBO from existing textures

        :param color_buffers: List of textures
        :param depth_buffer: Depth texture

        :return: FBO instance
        """
        instance = FBO()
        instance.color_buffers = color_buffers
        instance.depth_buffer = depth_buffer

        instance.fbo = context.ctx().framebuffer(
            [b.mgl_instance for b in color_buffers],
            depth_buffer.mgl_instance
        )

        return instance

    @staticmethod
    def create(size, components=4, depth=False, dtype='f1', layers=1):
        """
        Create a single or multi layer FBO

        :param size: (tuple) with and height
        :param components: (tuple) number of components. 1, 2, 3, 4
        :param depth: (bool) Create a depth attachment
        :param dtype: (string) data type per r, g, b, a ...
        :param layers: (int) number of color attachments

        :return: A new FBO
        """
        instance = FBO()

        # Add N layers of color attachments
        for layer in range(layers):
            c = Texture2D.create(size, components, dtype=dtype)
            instance.color_buffers.append(c)

        # Set depth attachment is specified
        if depth:
            instance.depth_buffer = DepthTexture(size)

        instance.fbo = context.ctx().framebuffer(
            [b.mgl_instance for b in instance.color_buffers],
            instance.depth_buffer.mgl_instance if instance.depth_buffer is not None else None
        )

        return instance

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
        self.fbo.use()

        if not stack:
            return

        FBO.stack.append(self)

        if len(FBO.stack) > 8:
            raise FBOError("FBO stack overflow. You probably forgot to release a bind somewhere.")

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

    def clear(self, red=0.0, green=0.0, blue=0.0, alpha=0.0, depth=1.0):
        """
        Clears the FBO using ``glClear``.
        """
        self.bind()
        self.fbo.clear(red=red, green=green, blue=blue, alpha=alpha, depth=depth)
        self.release()

    def draw_color_layer(self, layer=0, pos=(0.0, 0.0), scale=(1.0, 1.0)):
        """
        Draw a color layer in the FBO.
        :param layer: Layer ID
        :param pos: (tuple) offset x, y
        :param scale: (tuple) scale x, y
        """
        self.color_buffers[layer].draw(pos=pos, scale=scale)

    def draw_depth(self, near, far, pos=(0.0, 0.0), scale=(1.0, 1.0)):
        """
        Draw a depth buffer in the FBO.

        :param near: projection near.
        :param far: projection far.
        :param pos: (tuple) offset x, y
        :param scale: (tuple) scale x, y
        """
        self.depth_buffer.draw(near, far, pos=pos, scale=scale)

    def __repr__(self):
        return "<FBO {} color_attachments={} depth_attachement={}".format(
            self.fbo,
            self.color_buffers,
            self.depth_buffer,
        )


class FBOError(Exception):
    """Generic FBO Error"""
    pass
