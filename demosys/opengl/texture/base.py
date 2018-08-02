from typing import Tuple  # noqa

import moderngl
from demosys import context


def image_data(image):
    """Get components and bytes for an image"""
    # NOTE: We might want to check the actual image.mode
    #       and convert to an acceptable format.
    #       At the moment we load the data as is.
    data = image.tobytes()
    components = len(data) // (image.size[0] * image.size[1])
    return components, data


class BaseTexture:
    """
    Wraps the basic functionality of the ModernGL methods
    """
    def __init__(self):
        self.mglo = None  # Type: Union[moderngl.Texture, moderngl.TextureArray]

    @property
    def ctx(self) -> moderngl.Context:
        """ModernGL context"""
        return context.ctx()

    def use(self, location=0):
        """
        Bind the texture to a channel/location.

        :param location: The texture location. (GL_TEXTURE0 + location)
        """
        self.mglo.use(location)

    def build_mipmaps(self, base=0, max_level=1000):
        """
        Build mipmaps for this texture

        :param base: Level to build from
        :param max_level: Max levels
        """
        self.mglo.build_mipmaps(base=base, max_level=max_level)

    def read(self, level: int=0, alignment: int=1) -> bytes:
        """
        Read the content of the texture into a buffer.

        :param level: The mipmap level.
        :param alignment: The byte alignment of the pixels.
        :return: bytes
        """
        return self.mglo.read(level=level, alignment=alignment)

    def read_into(self, buffer: bytearray, level: int=0, alignment: int=1, write_offset: int=0):
        """
        Read the content of the texture into a buffer.

        :param buffer: (bytearray) The buffer that will receive the pixels.
        :param level: (int) The mipmap level.
        :param alignment: (int) The byte alignment of the pixels.
        :param write_offset: (int) The write offset.
        """
        self.mglo.read_into(buffer, level=level, alignment=alignment, write_offset=write_offset)

    def write(self, data: bytes, viewport=None, level: int=0, alignment: int=1):
        """
        Update the content of the texture.

        :param data: (bytes) – The pixel data.
        :param viewport: (tuple) – The viewport.
        :param level: (int) – The mipmap level.
        :param alignment: (int) – The byte alignment of the pixels.
        """
        self.mglo.write(data, viewport=viewport, level=level, alignment=alignment)

    def release(self):
        """Release/free the ModernGL object"""
        self.mglo.release()

    @property
    def size(self) -> Tuple:
        """The size of the texture"""
        return self.mglo.size

    @property
    def width(self) -> int:
        """int: Width of the texture"""
        return self.mglo.width

    @property
    def height(self) -> int:
        """int: Height of the texture"""
        return self.mglo.height

    @property
    def dtype(self) -> str:
        """str: The data type of the texture"""
        return self.mglo.dtype

    @property
    def components(self) -> int:
        """int: The number of components in the texture"""
        return self.mglo.components

    @property
    def samples(self) -> int:
        """int: The number of samples of the texture"""
        return self.mglo.samples

    @property
    def depth(self) -> bool:
        """Is this a depth texture?"""
        return self.mglo.depth

    @property
    def glo(self) -> int:
        """
        int: The internal OpenGL object.
        This values is provided for debug purposes only.
        """
        return self.mglo.glo

    @property
    def repeat_x(self):
        """bool: The repeat_x of the texture"""
        return self.mglo.repeat_x

    @repeat_x.setter
    def repeat_x(self, value):
        self.mglo.repeat_x = value

    @property
    def repeat_y(self):
        """bool: The repeat_y of the texture"""
        return self.mglo.repeat_y

    @repeat_y.setter
    def repeat_y(self, value):
        self.mglo.repeat_y = value

    @property
    def filter(self) -> Tuple[int, int]:
        """tuple: (min, mag) filtering of the texture"""
        return self.mglo.filter

    @filter.setter
    def filter(self, value):
        self.mglo.filter = value

    @property
    def anisotropy(self) -> float:
        """
        float: Number of samples for anisotropic filtering.
        Any value greater than 1.0 counts as a use of anisotropic filtering
        """
        return self.mglo.anisotropy

    @anisotropy.setter
    def anisotropy(self, value):
        self.mglo.anisotropy = value

    @property
    def swizzle(self):
        """str: The swizzle of the texture"""
        return self.mglo.swizzle

    @swizzle.setter
    def swizzle(self, value):
        self.mglo.swizzle = value
