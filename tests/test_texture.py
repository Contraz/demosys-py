from demosys.test import DemosysTestCase
from demosys.opengl import Texture2D, TextureArray, DepthTexture


class TextureTest(DemosysTestCase):

    def test_create(self):
        Texture2D.create((256, 256)).use()
        TextureArray.create((256, 256, 4)).use()
        DepthTexture.create((256, 256))

    def test_read(self):
        texture = Texture2D.create((4, 4), components=4)
        texture.read()

    def test_read_into(self):
        texture = Texture2D.create((4, 4), components=4)
        buff = bytearray([0] * 16 * 4)
        texture.read_into(buff)
