from demosys.loaders.texture.base import TextureLoader, image_data


class Loader(TextureLoader):
    name = 'array'

    def __init__(self, path=None, layers=None, **kwargs):
        super().__init__(path, **kwargs)
        self.layers = layers

        if self.layers is None:
            raise ValueError("TextureArray requires layers parameter")

    def load(self):
        """Load a texture array"""
        self._open_image()

        width, height, depth = self.image.size[0], self.image.size[1] // self.layers, self.layers
        components, data = image_data(self.image)

        texture = self.ctx.texture_array(
            (width, height, depth),
            components,
            data,
        )

        if self.mipmap:
            self.build_mipmaps()

        self._close_image()

        return texture
