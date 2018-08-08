Effect
======

.. py:module:: demosys.effects
.. py:currentmodule:: demosys.effects

The base Effect class extended in effect modules.

Draw Methods
------------

.. automethod:: Effect.draw(time, frametime, target)

Resource Methods
----------------

.. automethod:: Effect.get_program(label) -> ShaderProgram
.. automethod:: Effect.get_texture(label) -> Texture
.. automethod:: Effect.get_track(name) -> Track
.. automethod:: Effect.get_scene(label) -> Scene
.. automethod:: Effect.get_data(label) -> Any
.. automethod:: Effect.post_load()

Utility Methods
---------------

.. automethod:: Effect.create_projection(fov=75.0, near=1.0, far=100.0, ratio=None)
.. automethod:: Effect.create_transformation(rotation=None, translation=None)
.. automethod:: Effect.create_normal_matrix(modelview)

Attributes
----------

.. autoattribute:: Effect.ctx
.. autoattribute:: Effect.sys_camera
.. autoattribute:: Effect.name
.. autoattribute:: Effect.effect_name
.. autoattribute:: Effect.window
.. autoattribute:: Effect.runnable
