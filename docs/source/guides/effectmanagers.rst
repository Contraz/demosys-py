
Effect Managers
===============

An effect manager is responsible of:

- Instantiating effects
- Knowing what effect should be drawn based in some internal state
- Reading keyboard events if this is needed (optional)

You are fairly free to do what you want. Having control over
effect instantiation also means you can make multiple instances
of the same effect and assign different resources to them.

The most important part in the end is how you implement ``draw()``.

Some sane or insane examples to get started:

- Simply hard code what should run at what time or state
- A manger that cycles what effect is active based on a next/previous key
- Cycle effects based on a duration property you assign to them
- Load some external timer data describing what effect should run at what
  time. This can easily be done with rocket (we are planning to make a manager
  for this)
- You could just put all your draw code in the manager and not use effects
- Treat the manager as the main loop of a simple game

This is an example of the default ``SingleEffectManager``.

.. code-block:: python

   class SingleEffectManager(BaseEffectManger):
       """Run a single effect"""
       def __init__(self, effect_module=None):
           """
           Initalize the manager telling it what effect should run.

           :param effect_module: The effect module to run
           """
           self.active_effect = None
           self.effect_module = effect_module

       def pre_load(self):
           """
           Initialize the effect that should run.
           """
           # Instantiate all registered effects
           effect_list = [cfg.cls() for name, cfg in effects.effects.items()]
           # Find the single effect we are supposed to draw
           for effect in effect_list:
               if effect.name == self.effect_module:
                   self.active_effect = effect

           # Show some modest anger when we have been lied to
           if not self.active_effect:
               print("Cannot find effect '{}'".format(self.active_effect))
               print("Available effects:")
               print("\n".join(e.name for e in effect_list))
               return False
           return True

       def post_load(self):
           return True

       def draw(self, time, frametime, target):
           """This is called every frame by the framework"""
           self.active_effect.draw(time, frametime, target)

       def key_event(self, key, scancode, action, mods):
           """Called on most key presses"""
           print("SingleEffectManager:key_event", key, scancode, action, mods)

It's important to understand that ``pre_load`` is called before resources are
loaded and this is the correct place to instantiate effects. ``post_load``
is called right after loading is done.

The ``draw`` method is called every frame and you will have to send this to the
effect you want to draw.

The ``key_events`` method will trigger on key presses.

BaseEffectManger
^^^^^^^^^^^^^^^^

.. autoclass:: demosys.effects.managers.BaseEffectManger
   :members:
