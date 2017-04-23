
Effects
=======

In order to draw something to the screen using this framework you need to make one or multiple effects.
An effect is an independent python package of a certain format.

The Effect Package
^^^^^^^^^^^^^^^^^^

The effect package should have the following structure:

The effect Module
^^^^^^^^^^^^^^^^^


Effect Base Class
^^^^^^^^^^^^^^^^^

.. autoclass:: demosys.effects.effect.Effect
   :members:

Decorators
^^^^^^^^^^

.. autofunction:: demosys.effects.effect.bind_target
