
.. py:module:: demosys.effects
.. py:currentmodule:: demosys.effects

demosys.effects.Effect
======================

.. autodata:: Effect
   :annotation:

Initialization
--------------

.. automethod:: Effect.__init__
.. automethod:: Effect.post_load

Draw Methods
------------

.. automethod:: Effect.draw

Resource Methods
----------------

.. automethod:: Effect.get_texture
.. automethod:: Effect.get_program
.. automethod:: Effect.get_scene
.. automethod:: Effect.get_data
.. automethod:: Effect.get_effect
.. automethod:: Effect.get_effect_class
.. automethod:: Effect.get_track

Utility Methods
---------------

.. automethod:: Effect.create_projection
.. automethod:: Effect.create_transformation
.. automethod:: Effect.create_normal_matrix

Attributes
----------

.. autoattribute:: Effect.runnable
.. autoattribute:: Effect.ctx
.. autoattribute:: Effect.window
.. autoattribute:: Effect.sys_camera
.. autoattribute:: Effect.name
.. autoattribute:: Effect.label
