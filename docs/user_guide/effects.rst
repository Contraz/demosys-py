
Effects
=======

In order to actually render something to the screen you need to make one or
multiple effects. What these effects are doing is entirely up to you.
Effects have methods for fetching loaded resources and existing effect instances.
Effects can also create new instances of effects if needed. This would
happend during initialization.

Effect examples can be found in the ``examples`` directory in the root of the repository.

The Effect Package
------------------

The effect package should have the following structure (assuming our effect is
named "cube").

.. code-block:: bash

    cube
    ├── effects.py
    ├── dependencies.py
    └── resources
        └── programs
            └── cube
                └── cube.glsl
        └── textures
        └── scenes
        └── data

The ``effects.py`` module can contain one or multiple effects.
The effect package can also have no effects and all and only
provide resources for other effects to use. The ``effects.py``
module is still required to be present.

Dependencies
------------

The ``dependencies.py`` module is required to be present. It describes
its own resources and what effect packages it may depend on.

Example::

    from demosys.resources.meta import ProgramDescription

    effect_packages = 
        'full.python.path.to.another.package',
    ]

    resources = [
        ProgramDescription(label='cube_plain', path='cube_plain.glsl'),
    ]

Resources are given labels and effects can fetch them by this label.
When adding effect package dependencies we make the system aware
of this package so their resources are also loaded. The effects
in the depending package will also be registered in the system
and can be instantiated.

Resources
---------

The ``resources`` directory contains fixed directory names where resources
of specific types are supposed to be located. When an effect package is loaded
paths to these directories are added so the system can find them.

.. Note:: Notice that the resource directories contains another sub-directory
   with the same name as the effect package. This is because these
   folders are by default added to a project wide search path
   (for each resource type),
   so we should place it in a directory to reduce the chance of a name collisions.

Having resources in the effect package itself is entirely optional.
Resources can be located anywhere you want as long as you tell the system
where they can be found. This is covered in :doc:`/settings`.

Reasons to have resources in effect packages is to create an independent
resuable effect package you could even distribute. Also when a project
grows with lots of effect packages it can be nice to keep the effect
specific resources in the effect package they belong to instead of
putting all resources for the entire project in the same location.

The Effect base class have methods avaiable for fetching loaded resources.
See the :py:class:`demosys.effects.Effect`
