from typing import Any

from PIL import Image

from demosys.loaders.base import BaseLoader


class PillowLoader(BaseLoader):
    """Base loader using PIL/Pillow"""
    name = '__unknown__'

    def __init__(self, path, **kwargs):
        super().__init__(path)
        self.path = path
        self.kwargs = kwargs
        self.image = kwargs.get('image')
        self.flip = kwargs.get('flip') or True
        self.mipmap = kwargs.get('mipmap') or False

    def load(self) -> Any:
        raise NotImplementedError()

    def _open_image(self):
        self.image = Image.open(self.path)

        if self.flip:
            self.image = self.image.transpose(Image.FLIP_TOP_BOTTOM)

    def _close_image(self):
        self.image.close()


def image_data(image):
    """Get components and bytes for an image"""
    # NOTE: We might want to check the actual image.mode
    #       and convert to an acceptable format.
    #       At the moment we load the data as is.
    data = image.tobytes()
    components = len(data) // (image.size[0] * image.size[1])
    return components, data
