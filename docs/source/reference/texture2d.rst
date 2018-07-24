Texture2D
=========

.. py:module:: demosys.opengl
.. py:currentmodule:: demosys.opengl

.. autodata:: Texture2D
   :annotation:

Create
------

.. automethod:: Texture2D.create(size, components=4, data=None, samples=0, alignment=1, dtype='f1', mipmap=False) -> Texture2D
.. automethod:: Texture2D.from_image(path, image=None, **kwargs)

Methods
-------

.. automethod:: Texture2D.use(location=0)
.. automethod:: Texture2D.build_mipmaps(base=0, max_level=1000)
.. automethod:: Texture2D.set_image(image, flip=True)
.. automethod:: Texture2D.draw(pos=(0.0, 0.0), scale=(1.0, 1.0))
.. automethod:: Texture2D.read(level:int=0, alignment:int=1) -> bytes
.. automethod:: Texture2D.read_into(buffer:bytearray, level:int=0, alignment:int=1, write_offset:int=0)
.. automethod:: Texture2D.write(data:bytes, viewport=None, level:int=0, alignment:int=1)
.. automethod:: Texture2D.release()

Attributes
----------

.. autoattribute:: Texture2D.size
.. autoattribute:: Texture2D.width
.. autoattribute:: Texture2D.height
.. autoattribute:: Texture2D.dtype
.. autoattribute:: Texture2D.components
.. autoattribute:: Texture2D.samples
.. autoattribute:: Texture2D.repeat_x
.. autoattribute:: Texture2D.repeat_y
.. autoattribute:: Texture2D.filter
.. autoattribute:: Texture2D.anisotropy
.. autoattribute:: Texture2D.depth
.. autoattribute:: Texture2D.swizzle
.. autoattribute:: Texture2D.size
.. autoattribute:: Texture2D.ctx
.. autoattribute:: Texture2D.glo
