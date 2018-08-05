from demosys.loaders.texture.base import BaseLoader, image_data


class Texture2D(BaseLoader):
    name = '2d'

    def load(self):
        """Load a 2d texture"""
        if not self.image:
            self._open_image()

        components, data = image_data(self.image)

        texture = self.ctx.texture(
            self.image.size,
            components,
            data,
        )

        if self.mipmap:
            texture.build_mipmaps()

        self._close_image()

        return texture
