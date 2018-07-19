TextureArray
============

.. py:module:: demosys.opengl
.. py:currentmodule:: demosys.opengl

Create
------

.. automethod:: TextureArray.create(size, components=4, data=None, alignment=1, dtype='f1', mipmap=False) -> TextureArray

Methods
-------

.. automethod:: TextureArray.use(location=0)
.. automethod:: TextureArray.build_mipmaps(base=0, max_level=1000)
.. automethod:: TextureArray.set_image(image, flip=True)
.. automethod:: TextureArray.read(level:int=0, alignment:int=1) -> bytes
.. automethod:: TextureArray.read_into(buffer:bytearray, level:int=0, alignment:int=1, write_offset:int=0)
.. automethod:: TextureArray.write(data:bytes, viewport=None, level:int=0, alignment:int=1)
.. automethod:: TextureArray.release()

Attributes
----------

.. autoattribute:: TextureArray.size
.. autoattribute:: TextureArray.width
.. autoattribute:: TextureArray.height
.. autoattribute:: TextureArray.dtype
.. autoattribute:: TextureArray.samples
.. autoattribute:: TextureArray.components
.. autoattribute:: TextureArray.repeat_x
.. autoattribute:: TextureArray.repeat_y
.. autoattribute:: TextureArray.filter
.. autoattribute:: TextureArray.anisotropy

.. autoattribute:: TextureArray.depth
.. autoattribute:: TextureArray.swizzle
.. autoattribute:: TextureArray.size
.. autoattribute:: TextureArray.ctx
.. autoattribute:: TextureArray.glo
