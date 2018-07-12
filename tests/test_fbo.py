from demosys.test import DemosysTestCase
from demosys.opengl import FBO, Texture2D, DepthTexture

class FBOTest(DemosysTestCase):

    def test_create(self):
        fbo = FBO.create((256, 256), depth=True, layers=1)
        fbo.use()
        fbo.clear()
        fbo.release()

    def test_create_from_textures(self):
        fbo = FBO.create_from_textures(
            [
                Texture2D.create((256, 256)),
                Texture2D.create((256, 256)),
            ],
            DepthTexture.create(((256, 256))),
        )
        fbo.use()
        fbo.clear()
        fbo.release()
