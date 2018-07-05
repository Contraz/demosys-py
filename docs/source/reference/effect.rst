Effect
======

.. py:module:: demosys
.. py:currentmodule:: demosys.effects

Class
-----

.. autoclass:: Effect

Resource Methods
----------------

.. automethod:: Effect.draw(self, time, frametime, target)
.. automethod:: Effect.get_shader(self, path, local=False)
.. automethod:: Effect.get_texture(self, path, local=False, **kwargs)
.. automethod:: Effect.get_track(self, name, local=False)
.. automethod:: Effect.get_scene(self, path, local=False, **kwargs):

Utility Methods
---------------

.. automethod:: Effect.create_projection(self, fov=75.0, near=1.0, far=100.0, ratio=None)
.. automethod:: Effect.create_transformation(self, rotation=None, translation=None)
.. automethod:: Effect.create_normal_matrix(self, modelview)

Atrributes
----------

.. autoattribute:: Effect.ctx
.. autoattribute:: Effect.sys_camera
.. autoattribute:: Effect.name
.. autoattribute:: Effect.effect_name
.. autoattribute:: Effect.window_width
.. autoattribute:: Effect.window_height
.. autoattribute:: Effect.window_aspect
