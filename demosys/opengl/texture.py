import os
from OpenGL import GL
from OpenGL.GL.EXT import texture_filter_anisotropic as tfa
from PIL import Image


class Texture:
    """Represents a texture"""
    def __init__(self, name=None, path=None, width=0, height=0, depth=0, lod=0, target=GL.GL_TEXTURE_2D,
                 internal_format=GL.GL_RGBA8, format=GL.GL_RGBA, type=GL.GL_UNSIGNED_BYTE,
                 mipmap=False, anisotropy=0, min_filter=GL.GL_LINEAR, mag_filter=GL.GL_LINEAR,
                 wrap_s=GL.GL_CLAMP_TO_EDGE, wrap_t=GL.GL_CLAMP_TO_EDGE, wrap_r=GL.GL_CLAMP_TO_EDGE,
                 ):
        """Initialize texture without allocating data using default values"""
        self.texture = GL.glGenTextures(1)
        # dimensions
        self.width = width
        self.height = height
        self.depth = depth
        # format / type
        self.target = target
        self.lod = lod
        self.internal_format = internal_format
        self.format = format
        self.type = type
        self.wrap_s = wrap_s
        self.wrap_t = wrap_t
        self.wrap_r = wrap_r
        # filters
        self.min_filter = min_filter
        self.mag_filter = mag_filter
        self.anisotropy = float(anisotropy)
        self.mipmap = mipmap
        # Force mipmaps if anisotropy is specified
        if self.anisotropy > 0:
            self.mipmap = True
        # Ensure we are using the right interpolation modes
        if self.mipmap:
            self.min_filter = GL.GL_LINEAR_MIPMAP_LINEAR
            self.mag_filter = GL.GL_LINEAR
        # For pre-loading files
        self.name = name
        self.path = path

    @property
    def size(self):
        """
        Get the dimensions of the texture

        :return: (w, h) tuple
        """
        return self.width, self.height

    @classmethod
    def from_image(cls, path, image=None, **kwargs):
        """
        Creates and image from a image file using Pillow/PIL.
        Additional parameters is passed to the texture initializer.

        :param path: The path to the file
        :param image: The PIL/Pillow image object (Can be None)
        :return: Texture object
        """
        t = Texture(path=path, name=os.path.basename(path), **kwargs)
        if image:
            t.set_image(image)
        return t

    @classmethod
    def create_2d(cls, **kwargs):
        """
        Creates a 2d texture.
        All parameters are passed on the texture initializer.

        :return: Texture object
        """
        kwargs['target'] = GL.GL_TEXTURE_2D
        t = Texture(**kwargs)
        t._build()
        return t

    def bind(self):
        """
        Binds the texture to the currently active texture unit
        """
        GL.glBindTexture(self.target, self.texture)

    def _build(self, data=None):
        """Internal method for building the texture"""
        self.bind()
        GL.glTexParameteri(self.target, GL.GL_TEXTURE_MIN_FILTER, self.min_filter)
        GL.glTexParameteri(self.target, GL.GL_TEXTURE_MAG_FILTER, self.mag_filter)

        GL.glTexParameteri(self.target, GL.GL_TEXTURE_WRAP_S, self.wrap_s)
        GL.glTexParameteri(self.target, GL.GL_TEXTURE_WRAP_T, self.wrap_t)
        GL.glTexParameteri(self.target, GL.GL_TEXTURE_WRAP_R, self.wrap_r)

        if self.target == GL.GL_TEXTURE_2D:
            GL.glTexImage2D(self.target, self.lod, self.internal_format,
                            self.width, self.height, 0,
                            self.format, self.type, data)
        elif self.target == GL.GL_TEXTURE_1D:
            if self.width > self.height:
                GL.glTexImage1D(self.target, self.lod, self.internal_format,
                                self.width, 0, self.format, self.type, data)
            else:
                GL.glTexImage1D(self.target, self.lod, self.internal_format,
                                self.height, 0, self.format, self.type, data)

        if self.mipmap:
            GL.glGenerateMipmap(self.target)

        if self.anisotropy > 0:
            max_ani = GL.glGetFloatv(tfa.GL_MAX_TEXTURE_MAX_ANISOTROPY_EXT)
            self.anisotropy = min(max_ani, self.anisotropy)
            GL.glTexParameterf(self.target, tfa.GL_TEXTURE_MAX_ANISOTROPY_EXT, self.anisotropy)

    def set_image(self, image):
        """
        Set pixel data using a image file with PIL/Pillow.

        :param image: The PIL/Pillow image object
        """
        image_flipped = image.transpose(Image.FLIP_TOP_BOTTOM)
        data = image_flipped.convert("RGBA").tobytes()
        self.width, self.height = image.size
        if self.width == 1 or self.height == 1:
            self.target = GL.GL_TEXTURE_1D
        else:
            self.target = GL.GL_TEXTURE_2D
        self._build(data=data)

    def set_texture_repeat(self, wrap_s, wrap_t, wrap_r):
        """
        Sets the texture repeat mode

        :param wrap_s: Repeat mode S (glenum)
        :param wrap_t: Repeat mode T (glenum)
        :param wrap_r: Repeat mode R (glenum)
        """
        self.wrap_s = wrap_s
        self.wrap_t = wrap_t
        self.wrap_r = wrap_r

        self.bind()
        GL.glTexParameteri(self.target, GL.GL_TEXTURE_WRAP_S, self.wrap_s)
        GL.glTexParameteri(self.target, GL.GL_TEXTURE_WRAP_T, self.wrap_t)
        GL.glTexParameteri(self.target, GL.GL_TEXTURE_WRAP_R, self.wrap_r)

    def set_interpolation(self, min_filter, mag_filter):
        """
        Sets the texture interpolation mode

        :param min_filter: Min filter mode (glenum)
        :param mag_filter: Max filter mode (glenum)
        """
        self.min_filter = min_filter
        self.mag_filter = mag_filter
        self.bind()
        GL.glTexParameteri(self.target, GL.GL_TEXTURE_MIN_FILTER, self.min_filter)
        GL.glTexParameteri(self.target, GL.GL_TEXTURE_MAG_FILTER, self.mag_filter)
