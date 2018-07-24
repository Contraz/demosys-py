DepthTexture
============

.. py:module:: demosys.opengl
.. py:currentmodule:: demosys.opengl

.. autodata:: DepthTexture
   :annotation:

Create
------

.. automethod:: DepthTexture.create(size, data=None, samples=0, alignment=4) -> DepthTexture

Methods
-------

.. automethod:: DepthTexture.use(location=0)
.. automethod:: DepthTexture.draw(near, far, pos=(0.0, 0.0), scale=(1.0, 1.0))
.. automethod:: DepthTexture.read(level:int=0, alignment:int=1) -> bytes
.. automethod:: DepthTexture.read_into(buffer:bytearray, level:int=0, alignment:int=1, write_offset:int=0)
.. automethod:: DepthTexture.write(data:bytes, viewport=None, level:int=0, alignment:int=1)
.. automethod:: DepthTexture.release()

Attributes
----------

.. autoattribute:: DepthTexture.size
.. autoattribute:: DepthTexture.width
.. autoattribute:: DepthTexture.compare_func
.. autoattribute:: DepthTexture.height
.. autoattribute:: DepthTexture.dtype
.. autoattribute:: DepthTexture.components
.. autoattribute:: DepthTexture.samples
.. autoattribute:: DepthTexture.repeat_x
.. autoattribute:: DepthTexture.repeat_y
.. autoattribute:: DepthTexture.filter
.. autoattribute:: DepthTexture.anisotropy
.. autoattribute:: DepthTexture.depth
.. autoattribute:: DepthTexture.swizzle
.. autoattribute:: DepthTexture.size
.. autoattribute:: DepthTexture.ctx
.. autoattribute:: DepthTexture.glo
