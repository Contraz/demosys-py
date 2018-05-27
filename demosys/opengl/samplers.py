"""
Simple cached factory for creating samplers
"""
from OpenGL import GL
from OpenGL.GL.EXT import texture_filter_anisotropic as tfa


def create_sampler(mipmap=None, anisotropy=None,
                   min_filter=None, mag_filter=None,
                   wrap_s=None, wrap_t=None, wrap_r=None):
    """Create sampler or get from cache"""
    return Sampler(
        mipmap=mipmap,
        anisotropy=anisotropy,
        min_filter=min_filter,
        mag_filter=mag_filter,
        wrap_s=wrap_s,
        wrap_t=wrap_t,
        wrap_r=wrap_r,
    )


class Sampler:
    """Represents an immutable sampler we pre-set states"""
    def __init__(self, mipmap=None, anisotropy=None,
                 min_filter=None, mag_filter=None,
                 wrap_s=None, wrap_t=None, wrap_r=None):
        """Set sampler states"""
        self.sid = None
        self.mipmap = mipmap
        self.anisotropy = anisotropy
        self.min_filter = min_filter
        self.mag_filter = mag_filter
        self.wrap_s = wrap_s
        self.wrap_t = wrap_t
        self.wrap_r = wrap_r
        self.states()

    def bind(self, unit):
        GL.glBindSampler(unit, self.sid)

    def states(self):
        self.sid = GL.glGenSamplers(1)

        if self.wrap_s is not None:
            GL.glSamplerParameteri(self.sid, GL.GL_TEXTURE_WRAP_S, self.wrap_s)
        if self.wrap_t is not None:
            GL.glSamplerParameteri(self.sid, GL.GL_TEXTURE_WRAP_T, self.wrap_t)
        if self.wrap_r is not None:
            GL.glSamplerParameteri(self.sid, GL.GL_TEXTURE_WRAP_R, self.wrap_r)

        if self.mag_filter is not None:
            GL.glSamplerParameteri(self.sid, GL.GL_TEXTURE_MAG_FILTER, self.mag_filter)

        if self.mipmap:
            GL.glSamplerParameteri(self.sid, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR_MIPMAP_LINEAR)
        elif self.mipmap is not None:
            GL.glSamplerParameteri(self.sid, GL.GL_TEXTURE_MIN_FILTER, self.min_filter)

        if self.anisotropy is not None and self.anisotropy > 0:
            max_ani = GL.glGetFloatv(tfa.GL_MAX_TEXTURE_MAX_ANISOTROPY_EXT)
            self.anisotropy = min(max_ani, self.anisotropy)
            GL.glSamplerParameterf(self.sid, tfa.GL_TEXTURE_MAX_ANISOTROPY_EXT, self.anisotropy)
