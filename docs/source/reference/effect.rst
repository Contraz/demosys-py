Effect
======

The base Effect class extended in effect modules.

.. py:module:: demosys.effects
.. py:currentmodule:: demosys.effects

.. autoclass:: demosys.effects.Effect
   :members:
   :private-members:
   :special-members:


Draw Methods
------------

.. automethod:: Effect.draw(time, frametime, target)

Resource Methods
----------------

.. automethod:: Effect.get_shader(path, local=False) -> ShaderProgram
.. automethod:: Effect.get_texture(path, local=False, **kwargs) -> Texture2D
.. automethod:: Effect.get_track(name, local=False) -> Track
.. automethod:: Effect.get_scene(path, local=False, **kwargs) -> Scene

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
.. autoattribute:: Effect.window_size
.. autoattribute:: Effect.window_width
.. autoattribute:: Effect.window_height
.. autoattribute:: Effect.window_aspect

Decorators
----------

.. autofunction:: bind_target
