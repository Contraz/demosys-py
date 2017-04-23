
Effects
=======

In order to draw something to the screen using this framework you need to make one or
multiple effects. what these effects are doing is entirely up to you. Some like to
put everything into one effect and switch what they draw by flipping some internal
states, but this is probably not practical for more complex things.

An effect is a class with references to resources and a method for drawing.
An effect is an independent python package of specific format.

The Effect Package
^^^^^^^^^^^^^^^^^^

The effect package should have the following structure (assuming our effect is named "cube".

.. code-block:: bash

    cube
    ├── effect.py
    ├── shaders
    │   └── cube
    │       └── ...
    └── textures
        └── cube
            └── ...

The ``effect.py`` module is where the draw logic for the effect resides. Directories at the
same level are for resources for the effect. Notice that the resource directories contains
another directory with the name of the effect. This is because these folders are added to
a virtual directory (for each resource type) so we should place it in a directory to
reduce the change of name collisions. Two effects with the texture ``texture.png`` in
the root of their local ``textures/`` directory will cause the first effect to

Registry
^^^^^^^^

For an effect to be recognised by the system it has to be registered
in the ``EFFECTS`` tuple/list in your settings module.
Simply add the full python path to the package. If our cube example
above resides inside a ``myproject`` project package we need to add
the string ``myproject.cube``. See :doc:`settings`.

You can always run a single effect by using the ``runeffect`` command.

.. code-block:: bash

    ./manage.py runeffect myproject.cube

If you have multiple effects you need to crate or use an existing :doc:`effectmanagers`
that will decide what effect would be active at what time or state.

Resources
^^^^^^^^^

Resource loading is baked into the effect class it self. Methods are inherited
from the base ``Effect`` class such as ``get_shader`` and ``get_texture``.

Remember that you can also create global resource directories for all
the effects in your projects as well. This can be achieved by configuring
resource finders in :doc:`settings`.

The Effect Module
^^^^^^^^^^^^^^^^^

The effect module in an effect package needs to be named ``effect.py`` and
reside in the root of the package. It can only contain a single effect
class. The name of the class doesn't matter right now, but we are
considering allowing multiple effects in the future, so giving it
at least a descriptive name of that it represents is a good idea.

There are two important methods in an effect:
- ``__init__()``
- draw()

The **initializer** is called before resources are loaded. This is so the
effects can register the what resources they need. The resource
managers will return an empty object that will be populated when
loading starts.

The **draw** method is called by the framework or from a your custom
:doc:`effectmanagers` ever frame, or at least every frame the manager
decides the effect should be active at least.

The standard effect example:

.. code-block:: python

    from demosys.effects import effect
    from demosys.opengl import geometry
    from OpenGL import GL
    # from pyrr import matrix44

    class DefaultEffect(effect.Effect):
        """Generated default effect"""
        def __init__(self):
            self.shader = self.get_shader("default/default.glsl")
            self.cube = geometry.cube(4.0, 4.0, 4.0)

        @effect.bind_target
        def draw(self, time, frametime, target):
            GL.glEnable(GL.GL_DEPTH_TEST)

            # Rotate and translate
            m_mv = self.create_transformation(rotation=(time * 1.2, time * 2.1, time * 0.25),
                                              translation=(0.0, 0.0, -8.0))

            # Apply the rotation and translation from the system camera
            # m_mv = matrix44.multiply(m_mv, self.sys_camera.view_matrix)

            # Create normal matrix from model-view
            m_normal = self.create_normal_matrix(m_mv)

            # Draw the cube
            with self.cube.bind(self.shader) as shader:
                shader.uniform_mat4("m_proj", self.sys_camera.projection)
                shader.uniform_mat4("m_mv", m_mv)
                shader.uniform_mat3("m_normal", m_normal)
            self.cube.draw()

The parameters in the draw effect is:

- ``time``: The current time reported by our configured Timer in seconds.
- ``frametime``: The time a frame is expected to take in seconds.
  This is useful when you cannot use ``time``. Should be avoided.
- ``target`` is the target FBO of the effect

Time can potentially move at any speed or direction so it's good practice
to make sure the effect can run when time is moving in any direction.

The ``bind_target`` decorator is useful when you want to ensure
that an FBO passed to the effect is bound on entry and released on exit.
By default a fake FBO is passed in representing the window framebuffer.
EffectManagers can be used to pass in your own FBOs or another effect
can call ``draw(..)`` requesting the result to end up in the FBO it passes in
and then use this FBO as a texture on a cube.

Effect Base Class
^^^^^^^^^^^^^^^^^

.. autoclass:: demosys.effects.effect.Effect
   :members:

Decorators
^^^^^^^^^^

.. autofunction:: demosys.effects.effect.bind_target
