FBO
===

Framebuffer Object for off-screen rendering

.. py:module:: demosys.opengl
.. py:currentmodule:: demosys.opengl

Create
------

.. automethod:: FBO.create(size, components=4, depth=False, dtype='f1', layers=1) -> FBO
.. automethod:: FBO.create_from_textures(color_buffers:List[Texture2D], depth_buffer:DepthTexture=None) -> FBO

Methods
-------

.. automethod:: FBO.use(stack=True)
.. automethod:: FBO.release(stack=True)
.. automethod:: FBO.clear(red=0.0, green=0.0, blue=0.0, alpha=0.0, depth=1.0)
.. automethod:: FBO.draw_color_layer(layer=0, pos=(0.0, 0.0), scale=(1.0, 1.0))
.. automethod:: FBO.draw_depth(near, far, pos=(0.0, 0.0), scale=(1.0, 1.0))
.. automethod:: FBO.read(viewport=None, components=3, attachment=0, alignment=1, dtype='f1') -> bytes

Attributes
----------
.. autoattribute:: FBO.size
