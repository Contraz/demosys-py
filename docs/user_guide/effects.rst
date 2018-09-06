
Effects
=======

In order to actually render something to the screen you need to make one or
multiple effects. What these effects are doing is entirely up to you.
Effects have methods for fetching loaded resources and existing effect instances.
Effects can also create new instances of effects if needed. This would
happend during initialization.

Effect examples can be found in the `examples <https://github.com/Contraz/demosys-py/tree/master/examples>`_ directory in the root of the repository.

A bascic effect would have the following structure::

    from demosys.effects import Effect

    class MyEffect(Effect):

        def __init__(self):
            # Do initialization here

        def draw(self, time, frametime, target):
            # Called every frame the effect is active


The Effect Package
------------------

The effect package should have the following structure (assuming our effect package
is named "cube").

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
of specific types are supposed to be located. When an effect package is loaded,
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
grows with lots of effect packages it can be nice to keep effect specific
resources separate.

We currently support the following resource types:

* Shader programs
* Scene/mesh data (glfw 2.0 or wavefront obj)
* Textures (loaded with Pillow)
* Data (generic data loader supporting binary, text and json)

We load these resources by creating resource description instances::

    from demosys.resources.meta import (TextureDescription,
                                        ProgramDescription,
                                        SceneDescription,
                                        DataDescription)

    # Resource list in effect package or project
    resources = [
        # Textures
        TextureDescription(label="bricks", path="bricks.png"),
        TextureDescription(label="wood", path="bricks.png", mipmap=True),

        # Shader programs
        ProgramDescription(label="cube_plain", path="cube_plain.glsl"),
        ProgramDescription(
            label="cube_textured",
            vertex_shader="cube_textured.vs",
            fragment_shader="cube_textured.fs"
        ),

        # Scenes / Meshes
        SceneDescription(label="cube", path="cube.obj"),
        SceneDescription(label="sponza", path="sponza.gltf"),
        SceneDescription(label="test", path="test.glb"),

        # Generic data
        DataDescription(label="config", path="config.json", loader="json"),
        DataDescription(label="rawdata", path="data.dat", loader="binary"),
        DataDescription(label="random_text", path="info.txt", loader="text"),
    ]

The Effect base class have methods avaiable for fetching loaded resources by their label.
See the :py:class:`demosys.effects.Effect`.

There are no requirements to use the resource system, but it provides a convenient way
to ensure resources are only loaded once and are loaded and ready before effects starts
running. If you prefer to open files manually in an effect initializer with ``open``
you are free to do that.

You can also load resources directly at an point in time by using the ``resources`` package::

    from demosys.resources import programs, textures, scenes, data
    from demosys.resources.meta import (TextureDescription,
                                        ProgramDescription,
                                        SceneDescription,
                                        DataDescription)

    program = programs.load(ProgramDescription(label="cube_plain", path="cube_plain.glsl"))
    texture = textures.load(TextureDescription(label="bricks", path="bricks.png"))
    scene = scenes.load(SceneDescription(label="cube", path="cube.obj"))
    config = data.load(DataDescription(label="config", path="config.json", loader="json"))

This is not recommended, but in certain instances it can be unavoidable. An example
could be loading a piece of data that references other resources. These are common
to use in resource loader classes. Also, if you for some reason need to load something
while effects are already, this would be the solution.

Running an Effect Package
-------------------------

Effect packages can be run by using the ``runeffect`` command::

    python manage.py runeffect <python.path.to.package>

    # Example
    python manage.py runeffect examples.cubes

This will currently look for the first effect class with the ``runnable`` attribute set to ``True``,
make an instance of that effect and call its ``draw`` method every frame. The effect package
dependencies are also handled. (All handled by ``DefaultProject`` class)

The runnable effect is resposible for instantiating other effects it depends on and call them
directly.

Optionally you can also specify the exact effect to run in the effect package
by adding the class name to the path::

    python manage.py runeffect <python.path.to.package>.<effect class name>

    # Example
    python manage.py runeffect examples.cubes.Cubes

If you need a more complex setup where multiple runnable effects are involved, you need
to create a proper project config using ``project.py`` and instead use the ``run`` command.
