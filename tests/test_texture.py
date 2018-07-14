import moderngl

from demosys.test import DemosysTestCase
from demosys.opengl import Texture2D, TextureArray, DepthTexture


class TextureTest(DemosysTestCase):

    def test_create(self):
        texture = Texture2D.create((256, 256))
        self.assertProperties(texture)

        array = TextureArray.create((256, 256, 4))
        self.assertProperties(array)

        depth_texture = DepthTexture.create((256, 256))
        self.assertProperties(depth_texture)

    def test_read(self):
        texture = Texture2D.create((4, 4), components=4)
        texture.read()

    def test_read_into(self):
        texture = Texture2D.create((4, 4), components=4)
        buff = bytearray([0] * 16 * 4)
        texture.read_into(buff)

    def assertProperties(self, texture):
        """Poke all the common properties"""
        texture.use()
        # FIXME: size for texture array bug in ModernGL
        if not isinstance(texture, TextureArray):
            assert texture.size == (256, 256)
            assert texture.width == 256
            assert texture.height == 256
            assert texture.components > 0

            texture.filter = moderngl.LINEAR, moderngl.LINEAR
    
            assert isinstance(texture.dtype, str)

            if not texture.depth:
                assert texture.swizzle == 'RGBA'

        assert isinstance(texture.ctx, moderngl.Context)
        assert isinstance(texture.glo, int)

        texture.repeat_x = False
        texture.repeat_y = True
        assert texture.repeat_x is False
        assert texture.repeat_y is True
