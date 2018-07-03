"""
Simple cached factory for creating samplers
"""
import OpenGL
OpenGL.ERROR_CHECKING = False  # noqa

from OpenGL import GL
from OpenGL.GL.EXT import texture_filter_anisotropic as tfa


def create(mipmap=None, anisotropy=None,
           min_filter=None, mag_filter=None,
           wrap_s=None, wrap_t=None, wrap_r=None,
           texture_compare_mode=None,
           texture_compare_func=None):
    """Create sampler or get from cache"""
    return Sampler(
        mipmap=mipmap,
        anisotropy=anisotropy,
        min_filter=min_filter,
        mag_filter=mag_filter,
        wrap_s=wrap_s,
        wrap_t=wrap_t,
        wrap_r=wrap_r,
        texture_compare_mode=texture_compare_mode,
        texture_compare_func=texture_compare_func,
    )


class Sampler:
    """Represents an immutable sampler we pre-set states"""
    def __init__(self, mipmap=None, anisotropy=None,
                 min_filter=None, mag_filter=None,
                 wrap_s=None, wrap_t=None, wrap_r=None,
                 texture_compare_mode=None, texture_compare_func=None):
        """Set sampler states"""
        self._id = None

        self.mipmap = mipmap
        self.anisotropy = anisotropy
        self.min_filter = min_filter
        self.mag_filter = mag_filter
        self.wrap_s = wrap_s
        self.wrap_t = wrap_t
        self.wrap_r = wrap_r
        self.texture_compare_mode = texture_compare_mode
        self.texture_compare_func = texture_compare_func

        self.states()

    def use(self, location=0):
        GL.glBindSampler(location, self._id)

    def release(self, location=0):
        GL.glBindSampler(location, 0)

    def states(self):
        self._id = GL.glGenSamplers(1)

        if self.wrap_s is not None:
            GL.glSamplerParameteri(self._id, GL.GL_TEXTURE_WRAP_S, self.wrap_s)
        if self.wrap_t is not None:
            GL.glSamplerParameteri(self._id, GL.GL_TEXTURE_WRAP_T, self.wrap_t)
        if self.wrap_r is not None:
            GL.glSamplerParameteri(self._id, GL.GL_TEXTURE_WRAP_R, self.wrap_r)

        if self.min_filter is not None:
            GL.glSamplerParameteri(self._id, GL.GL_TEXTURE_MIN_FILTER, self.min_filter)

        if self.mag_filter is not None:
            GL.glSamplerParameteri(self._id, GL.GL_TEXTURE_MAG_FILTER, self.mag_filter)

        if self.mipmap:
            GL.glSamplerParameteri(self._id, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR_MIPMAP_LINEAR)

        if self.anisotropy is not None and self.anisotropy > 0:
            max_ani = GL.glGetFloatv(tfa.GL_MAX_TEXTURE_MAX_ANISOTROPY_EXT)
            self.anisotropy = min(max_ani, self.anisotropy)
            GL.glSamplerParameterf(self._id, tfa.GL_TEXTURE_MAX_ANISOTROPY_EXT, self.anisotropy)

        if self.texture_compare_mode is False:
            GL.glSamplerParameteri(self._id, GL.GL_TEXTURE_COMPARE_MODE, GL.GL_NONE)
        elif self.texture_compare_mode is True:
            GL.glSamplerParameteri(self._id, GL.GL_TEXTURE_COMPARE_MODE, GL.GL_COMPARE_REF_TO_TEXTURE)
