
Timers
======

Timers are classes keeping track of time passing the value
to the effect's ``draw`` methods. We should assume that time can move
in any direction at any speed. Time is always reported as a float in
seconds.

The default timer if not specified in settings:

.. code-block:: shell

    TIMER = 'demosys.timers.Timer'

This is a simple timer starting at 0 when effects start drawing.
All timers should respond correctly to pause ``SPACE``.

Standard Timers
---------------

- ``demosys.timers.Timer``: Default timer just tracking time in seconds
- ``demosys.timers.Music``: Timer playing music reporting duration in the song
- ``demosys.timers.RocketTimer``: Timer using the rocket sync system
- ``demosys.timers.RocketMusicTimer``: Timer using the rocket sync system with
  music playback

Custom Timer
------------

You create a custom timer by extending ``demosys.timers.base.BaseTimer``.

.. autoclass:: demosys.timers.base.BaseTimer
   :members:
