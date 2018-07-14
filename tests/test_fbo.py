from demosys.test import DemosysTestCase
from demosys.opengl import FBO, Texture2D, DepthTexture


class FBOTest(DemosysTestCase):

    def test_create(self):
        fbo = FBO.create((256, 256), depth=True, layers=1)
        self.assertGeneral(fbo)

    def test_create_from_textures(self):
        fbo = FBO.create_from_textures(
            [
                Texture2D.create((256, 256)),
                Texture2D.create((256, 256)),
            ],
            DepthTexture.create(((256, 256))),
        )

    def test_read(self):
        fbo = FBO.create((256, 256), depth=True, layers=1)

        data = fbo.read(components=4)
        assert len(data) == 256 * 256 * 4

        buffer = bytearray([0] * 256 * 256 * 4)
        fbo.read_into(buffer)

    def assertGeneral(self, fbo):
        assert fbo.viewport
        fbo.viewport = 0, 0, fbo.size[0], fbo.size[1]
        assert fbo.color_mask == (True, True, True, True)
        fbo.color_mask = (False, False, True, True)
        assert fbo.depth_mask == True
        fbo.depth_mask = False
        assert fbo.samples == 0

        fbo.use()
        fbo.clear()
        fbo.release()
