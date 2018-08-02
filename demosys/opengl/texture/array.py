from PIL import Image

from demosys import context

from .base import BaseTexture, image_data


class TextureArray(BaseTexture):
    """
    A TextureArray is a texture where each mipmap level contains an array of
    images of the same size. Array textures may have Mipmaps, but each mipmap
    in the texture has the same number of levels.

    The image data size must exactly match (width, height * layers)
    """

    def __init__(self, path: str=None, mipmap: bool=False, layers=0, **kwargs) -> 'TextureArray':
        """
        Initialize configuration for this texture.
        This doesn't create the OpenGL texture objects itself
        and is mostly used by the resource loading system.

        :param path: The global resource path for the texture to load
        :param mipmap: (bool) Should we generate mipmaps?
        """
        super().__init__()
        # Info for resource loader
        self.path = path
        self.layers = layers
        self.mipmap = mipmap

        if self.layers <= 0:
            raise ValueError("Texture {} requires a layer parameter > 0".formats(self.path))

    @classmethod
    def create(cls, size, components=4, data=None, alignment=1, dtype='f1', mipmap=False) -> 'TextureArray':
        """
        :param size: (x, y, layers) size and layers of the texture
        :param components: The number of components 1, 2, 3 or 4
        :param data: (bytes) Content of the texture
        :param alignment: The byte alignment 1, 2, 4 or 8
        :param dtype: (str) The data type
        :param mipmap: (bool) Generate mipmaps
        :returns: :py:class:`TextureArray` object
        """
        texture = TextureArray("create", mipmap=False, layers=size[2])
        texture.mglo = context.ctx().texture_array(
            size, components,
            data=data, alignment=alignment, dtype=dtype,
        )

        if mipmap:
            texture.build_mipmaps()

        return texture

    def set_image(self, image, flip=True):
        """
        Set pixel data using a image file with PIL/Pillow.
        The image size must exactly match (width, height * layers)

        :param image: The PIL/Pillow image object
        :param flip: Flip the image top to bottom
        """
        if flip:
            image = image.transpose(Image.FLIP_TOP_BOTTOM)

        width, height, depth = image.size[0], image.size[1] // self.layers, self.layers
        components, data = image_data(image)

        self.mglo = self.ctx.texture_array(
            (width, height, depth),
            components,
            data,
        )

        if self.mipmap:
            self.build_mipmaps()
