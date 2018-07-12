from typing import List

from demosys import context
from demosys.opengl import DepthTexture, Texture2D


class WindowFBO:
    window = None

    @classmethod
    def use(cls):
        """Sets the viewport back to the buffer size of the screen/window"""
        cls.window.use()
        cls.window.viewport()

    @classmethod
    def release(cls):
        """Dummy release method"""
        pass

    @classmethod
    def clear(cls, red=0.0, green=0.0, blue=0.0, depth=1.0, viewport=None):
        """Dummy clear method"""
        cls.window.clear()

    @property
    @classmethod
    def mglo(cls):
        """Internal ModernGL fbo"""
        return cls.window.mgl_fbo()


class FBO:
    """Frame buffer object"""
    _stack = []

    def __init__(self):
        self.color_buffers = []
        self.depth_buffer = None
        self.fbo = None

    @staticmethod
    def create_from_textures(color_buffers: List[Texture2D], depth_buffer: DepthTexture = None) -> 'FBO':
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
            color_attachments=[b.mglo for b in color_buffers],
            depth_attachment=depth_buffer.mglo if depth_buffer is not None else None,
        )

        return instance

    @staticmethod
    def create(size, components=4, depth=False, dtype='f1', layers=1) -> 'FBO':
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
        for _ in range(layers):
            tex = Texture2D.create(size, components, dtype=dtype)
            instance.color_buffers.append(tex)

        # Set depth attachment is specified
        if depth:
            instance.depth_buffer = DepthTexture(size)

        instance.fbo = context.ctx().framebuffer(
            color_attachments=[b.mglo for b in instance.color_buffers],
            depth_attachment=instance.depth_buffer.mglo if instance.depth_buffer is not None else None
        )

        return instance

    def read(self, viewport=None, components=3, attachment=0, alignment=1, dtype='f1') -> bytes:
        """
        Read the content of the framebuffer.

        :param viewport: (tuple) The viewport
        :param components: The number of components to read.
        :param attachment: The color attachment
        :param alignment: The byte alignment of the pixels
        :param dtype: (str) dtype
        """
        return self.fbo.read(
            viewport=viewport,
            components=components,
            attachment=attachment,
            alignment=alignment,
            dtype=dtype,
        )

    @property
    def size(self):
        """
        Attempts to determine the pixel size of the FBO.
        Currently returns the size of the first color attachment.
        If the FBO has no color attachments, the depth attachment will be used.
        Raises ``FBOError`` if the size cannot be determined.

        :return: (w, h) tuple representing the size in pixels
        """
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
        self.use()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit context manager.
        This will release the FBO.
        """
        self.release()

    def use(self, stack=True):
        """
        Bind FBO adding it to the stack.

        :param stack: (bool) If the bind should push the current FBO on the stack.
        """
        self.fbo.use()

        if not stack:
            return

        FBO._stack.append(self)

        if len(FBO._stack) > 8:
            raise FBOError("FBO stack overflow. You probably forgot to release a bind somewhere.")

    def release(self, stack=True):
        """
        Bind FBO popping it from the stack

        :param stack: (bool) If the bind should be popped form the FBO stack.
        """
        if not stack:
            WindowFBO.use()
            return

        # Are we trying to release an FBO that is not bound?
        if not FBO._stack:
            raise FBOError("FBO stack is already empty. You are probably releasing a FBO twice or forgot to bind.")

        fbo_out = FBO._stack.pop()

        # Make sure we released this FBO and not some other random one
        if fbo_out != self:
            raise FBOError("Incorrect FBO release order")

        # Find the parent fbo
        if FBO._stack:
            parent = FBO._stack[-1]
        else:
            parent = WindowFBO

        # Bind the parent FBO
        if parent:
            parent.use()

    def clear(self, red=0.0, green=0.0, blue=0.0, alpha=0.0, depth=1.0):
        """
        Clears all FBO layers including depth
        """
        self.use()
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

    @property
    def mglo(self):
        """Internal ModernGL fbo"""
        return self.fbo


class FBOError(Exception):
    """Generic FBO Error"""
    pass
