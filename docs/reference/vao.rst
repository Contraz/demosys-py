VAO
===

.. py:module:: demosys.opengl.vao
.. py:currentmodule:: demosys.opengl.vao

.. autoclass:: VAO

Create
------

.. automethod:: VAO.__init__
.. automethod:: VAO.buffer(buffer, buffer_format:str, attribute_names, per_instance=False)
.. automethod:: VAO.index_buffer(buffer, index_element_size=4)

Render Methods
--------------

.. automethod:: VAO.render(program:Program, mode=None, vertices=-1, first=0, instances=1)
.. automethod:: VAO.render_indirect(program:Program, buffer, mode=None, count=-1, first=0)
.. automethod:: VAO.transform(program:Program, buffer:Buffer, mode=None, vertices=-1, first=0, instances=1)

Other Methods
-------------

.. automethod:: VAO.instance(program:Program) -> VertexArray
.. automethod:: VAO.release(buffer=True)
