VAO
===

.. py:module:: demosys.opengl.vao
.. py:currentmodule:: demosys.opengl.vao

.. autoclass:: VAO

Create
------

.. automethod:: VAO.__init__
.. automethod:: VAO.buffer
.. automethod:: VAO.index_buffer

Render Methods
--------------

.. automethod:: VAO.render
.. automethod:: VAO.render_indirect
.. automethod:: VAO.transform

Other Methods
-------------

.. automethod:: VAO.instance(program:Program) -> VertexArray
.. automethod:: VAO.release(buffer=True)
