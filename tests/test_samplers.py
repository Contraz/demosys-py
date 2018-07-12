from demosys.test import DemosysTestCase
from demosys.opengl import samplers, Sampler
from OpenGL import GL


class SamplerTest(DemosysTestCase):

    def test_create(self):
        args = {
            "mipmap": True,
            "anisotropy": 4,
            "min_filter": GL.GL_LINEAR,
            "mag_filter": GL.GL_LINEAR,
            "wrap_s": GL.GL_CLAMP_TO_EDGE,
            "wrap_t": GL.GL_CLAMP_TO_EDGE,
            "wrap_r": GL.GL_CLAMP_TO_EDGE,
            "texture_compare_mode": GL.GL_NONE,
            "texture_compare_func": GL.GL_NONE,
        }
        s_1 = samplers.create(**args)
        s_2 = Sampler(**args)

        s_1.use()
        s_2.use()

        s_1.release()
