from PIL import Image

from demosys import context


class BaseLoader:
    name = None

    def __init__(self, path, **kwargs):
        self.path = path
        self.kwargs = kwargs
        self.image = kwargs.get('image')
        self.flip = kwargs.get('flip') or True
        self.mipmap = kwargs.get('mipmap') or False

    def load(self):
        pass

    def _open_image(self):
        self.image = Image.open(self.path)

        if self.flip:
            self.image = self.image.transpose(Image.FLIP_TOP_BOTTOM)

    def _close_image(self):
        self.image.close()

    @property
    def ctx(self):
        return context.ctx()


def image_data(image):
    """Get components and bytes for an image"""
    # NOTE: We might want to check the actual image.mode
    #       and convert to an acceptable format.
    #       At the moment we load the data as is.
    data = image.tobytes()
    components = len(data) // (image.size[0] * image.size[1])
    return components, data
