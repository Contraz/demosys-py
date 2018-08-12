VAO
===

.. py:module:: demosys.opengl
.. py:currentmodule:: demosys.opengl

.. autoclass:: VAO

Methods
-------

.. automethod:: VAO.buffer(buffer, buffer_format:str, attribute_names, per_instance=False)
.. automethod:: VAO.index_buffer(buffer, index_element_size=4)
.. automethod:: VAO.subroutines(shader, routines:tuple)
.. automethod:: VAO.release(buffer=True)

Draw Methods
------------

.. automethod:: VAO.draw(program:Program, mode=None, vertices=-1, first=0, instances=1)
.. automethod:: VAO.transform(program:Program, buffer:Buffer, mode=None, vertices=-1, first=0, instances=1)
