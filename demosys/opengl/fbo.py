from typing import List, Tuple

from demosys import context
from demosys.opengl import DepthTexture, Texture2D


class FBO:
    """
    A framebuffer object is a collection of buffers that can be used as the destination for rendering.
    The buffers for framebuffer objects reference images from either textures.

    A typical FBO has one or multiple color layers and a depth. Shaders can write to these buffers
    when activated.
    """
    _stack = []

    def __init__(self):
        self._window = context.window()
        self.color_buffers = []
        self.depth_buffer = None
        self.fbo = None
        self.default_framebuffer = False

    @staticmethod
    def create_from_textures(color_buffers: List[Texture2D], depth_buffer: DepthTexture = None) -> 'FBO':
        """
        Create FBO from existing textures

        :param color_buffers: List of textures
        :param depth_buffer: Depth texture

        :return: A new :py:class:`FBO`
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
        :return: A new :py:class:`FBO`
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

    def read_into(self, buffer, viewport=None, components=3,
                  attachment=0, alignment=1, dtype='f1', write_offset=0):
        """
        Read the content of the framebuffer into a buffer.

        :param buffer: (bytearray) The buffer that will receive the pixels.
        :param viewport: (tuple) The viewport.
        :param components: (int) The number of components to read.
        :param attachment: (int) The color attachment.
        :param alignment: (int) The byte alignment of the pixels.
        :param dtype: (str) Data type.
        :param write_offset: (int) The write offset.
        """
        return self.fbo.read_into(
            buffer,
            viewport=viewport,
            components=components,
            attachment=attachment,
            alignment=alignment,
            dtype=dtype,
            write_offset=write_offset
        )

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
        Optionally a context manager can be used:

        optonally a context manager can be used::

            with fbo:
                # draw stuff

        :param stack: (bool) If the bind should push the current FBO on the stack.
        """
        self.fbo.use()

        if not stack:
            return

        if not self.default_framebuffer:
            FBO._stack.append(self)

        if len(FBO._stack) > 8:
            raise FBOError("FBO stack overflow. You probably forgot to release a bind somewhere.")

    def release(self, stack=True):
        """
        Bind FBO popping it from the stack

        :param stack: (bool) If the bind should be popped form the FBO stack.
        """
        if self.default_framebuffer:
            return

        if not stack:
            self._window.fbo.use()
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
            parent = self._window.fbo

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
    def size(self):
        """
        (w, h) tuple representing the size in pixels
        """
        return self.fbo.size

    @property
    def samples(self) -> int:
        """
        int: The samples of the framebuffer.
        """
        return self.fbo.samples

    @property
    def viewport(self) -> Tuple[int, int, int, int]:
        """
        tuple: The viewport of the framebuffer.
        """
        return self.mglo.viewport

    @viewport.setter
    def viewport(self, value):
        self.fbo.viewport = tuple(value)

    @property
    def color_mask(self) -> Tuple[bool, bool, bool, bool]:
        """
        tuple[bool, bool, bool, bool]: The color mask of the framebuffer.
        """
        return self.mglo.color_mask

    @color_mask.setter
    def color_mask(self, value):
        self.fbo.color_mask = value

    @property
    def depth_mask(self) -> bool:
        """
        bool: The depth mask of the framebuffer.
        """
        return self.mglo.depth_mask

    @depth_mask.setter
    def depth_mask(self, value):
        self.fbo.depth_mask = value

    @property
    def mglo(self):
        """Internal ModernGL fbo"""
        return self.fbo


class FBOError(Exception):
    """Generic FBO Error"""
    pass
