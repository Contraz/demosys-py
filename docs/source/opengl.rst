
OpenGL Objects
==============

We proved some simple and powerful wrappers over OpenGL features in the
``demosys.opengl`` package.

- **Texture**: Textures from images or manually constructed/generated
- **Shader**: Shader programs currently supporting vertex/fragment/geometry shaders
- **Frame Buffer Object**: Offscreen rendering targets represented as textures
- **Vertex Array Object**: Represents the geometry we are drawing using a shader

Texture
^^^^^^^

Textures are normally loaded by requesting the resource by path/name in the initializer
of an effect using the ``self.get_texture`` method inherited from the ``Effect`` base class.
We use the PIL/Pillow library to image data from file.

Textures can of course also be crated manually if needed.

.. autoclass:: demosys.opengl.texture.Texture
    :members:
    :undoc-members:
    :show-inheritance:

Shader
^^^^^^

In oder to draw something to the screen, we need a shader. There is no other way.

Shader should ideally always be loaded from ``.glsl`` files located in a ``shaders`` directory
in your effect or project global resource directory. Shaders have to be written in a single
file were the different shader types are separated using preprocessors.

.. Note:: We wish to support loading shaders in other common formats such
   as separate files for each shader type. Feel free to make a pull request
   or create an issue on github.

Like textures they are loaded in the effect using the ``get_shader`` method in the initializer.

Once we have the reference to the shader object we will need a VAO object
in order to bind it. We could of course just call ``bind()``, but **the VAOs
will do this for you**. More details in the VAO section below.

.. code-block:: glsl

    #version 410

    #if defined VERTEX_SHADER
    // Vertex shader here
    #elif defined FRAGMENT_SHADER
    // Fragment shader here
    #elif defined GEOMETRY_SHADER
    // Geometry shader here
    #endif

Once the shader is bound we can set uniforms through the various ``uniform_`` methods.

Assuming we have a reference to a shader in ``s``:

.. code-block:: python

    # Set the uniform (float) with name 'value' to 1.0
    s.uniform_1f("value", 1.0)
    # Set the uniform (mat4) with name `m_view' to a 4x4 matrix
    s.uniform_mat4("m_view", view_matrix)
    # Set the sampler2d uniform to use a Texture object we have loaded
    s.sampler_2d(0, "texture0", texture)

The Shader class contains an internal cache of all the uniform variables
the shader has, so it will generally do very efficient type checks at run time
and give useful error feedback if something is wrong.

Other than setting uniforms and using the right file format for shaders, there
are not much more to them.

.. Note:: We are planning to support passing in preprocessors to shader.
   Please make an issue or a pull request on github.

.. autoclass:: demosys.opengl.shader.Shader
    :members:
    :undoc-members:
    :show-inheritance:

Vertex Array Object
^^^^^^^^^^^^^^^^^^^

Vertex Array Objects represents the geometry we are drawing with shaders.
They keep track of the buffer binding states of one or multiple Vertex
Buffer Objects.

VAOs and shaders interact in a very important way. The first time the VAO
and shader interacts, they will figure out if they are compatible when it
comes to the attributes in the shader and the buffers in the VAO.

When we create VAOs we tell explicitly what attribute name each buffer belongs to.

Example: I have three buffers representing positions, normals and uvs.

- Map positions to ``in_position`` attribute with 3 components
- Map normals to ``in_normal`` attribute with 3 components
- Map uvs to the ``in_uv`` attribute with 2 components

The vertex shader will have to define the exact same attribute names:

.. code-block:: glsl

    in vec3 in_position;
    in vec3 in_normal;
    in vec2 in_uv

This is not entirely true. The shader will at least have to define
the ``in_position``. The other two attributes are optional. This
is were the VAO and the Shader negotiates the attribute binding.
The VAO object will on-the-fly generate a version of itself that
supports the shaders attributes.

The VAO/Shader binding can also be used as a context manager as seen below,
but this is optional. The context manager will return the reference to
the shader so you can use a shorter name.

.. code-block:: python

    # Without context manager
    vao.bind(shader)
    shader.unform_1f("value", 1.0)
    vao.draw()

    # Bind the shader and negotiate attribute binding
    with vao.bind(shader) as s:
        s.unform_1f("value", 1.0)
        # ...
    # Finally draw the geometry
    vao.draw()

When creating a VBO we need to use the `OpenGL.arrays.vbo.VBO instance` in
PyOpenGL. We pass a numpy array to the constructor. It's important to use
the correct ``dtype`` so it matches the type passed in ``add_array_buffer``.

Each VBO is first added to the VAO using ``add_array_buffer``. This is simply
to register the buffer and tell the VAO what format it has.

The ``map_buffer`` part will define the actual attribute mapping.
Without this the VAO is not complete.

Calling ``build()`` will finalize and sanity check the VAO.

The VAO initializer also takes an optional argument ``mode``
were you can specify what the default draw mode is. This can
be overridden in ``draw(mode=...)``.

The VAO will always do **very** strict error checking and give
useful feedback when something is wrong. VAOs must also be
assigned a name so the framework can reference it in error messages.

.. code-block:: python

    def quad_2d(width, height, xpos, ypos):
        """
        Creates a 2D quad VAO using 2 triangles.

        :param width: Width of the quad
        :param height: Height of the quad
        :param xpos: Center position x
        :param ypos: Center position y
        """
        pos = VBO(numpy.array([
            xpos - width / 2.0, ypos + height / 2.0, 0.0,
            xpos - width / 2.0, ypos - height / 2.0, 0.0,
            xpos + width / 2.0, ypos - height / 2.0, 0.0,
            xpos - width / 2.0, ypos + height / 2.0, 0.0,
            xpos + width / 2.0, ypos - height / 2.0, 0.0,
            xpos + width / 2.0, ypos + height / 2.0, 0.0,
        ], dtype=numpy.float32))
        normals = VBO(numpy.array([
            0.0, 0.0, 1.0,
            0.0, 0.0, 1.0,
            0.0, 0.0, 1.0,
            0.0, 0.0, 1.0,
            0.0, 0.0, 1.0,
            0.0, 0.0, 1.0,
        ], dtype=numpy.float32))
        uvs = VBO(numpy.array([
            0.0, 1.0,
            0.0, 0.0,
            1.0, 0.0,
            0.0, 1.0,
            1.0, 0.0,
            1.0, 1.0,
        ], dtype=numpy.float32))
        vao = VAO("geometry:quad", mode=GL.GL_TRIANGLES)
        vao.add_array_buffer(GL.GL_FLOAT, pos)
        vao.add_array_buffer(GL.GL_FLOAT, normals)
        vao.add_array_buffer(GL.GL_FLOAT, uvs)
        vao.map_buffer(pos, "in_position", 3)
        vao.map_buffer(normals, "in_normal", 3)
        vao.map_buffer(uvs, "in_uv", 2)
        vao.build()
        return vao

We can also pass index/element buffers to VAOs. We can also use
interleaved VBOs by passing the same VBO to ``map_buffer`` multiple
times.

More examples can be found in the :doc:`geometry` module.

.. autoclass:: demosys.opengl.vao.VAO
    :members:
    :undoc-members:
    :show-inheritance:

Frame Buffer Object
^^^^^^^^^^^^^^^^^^^

Frame Buffer Objects are offscreen render targets.
Internally they are simply textures that can be used further in rendering.
FBOs can even have multiple layers so a shader can write to multiple buffers at once.
They can also have depth/stencil buffers. Currently we use
use a depth 24 / stencil 8 buffer by default as the depth format.

Creating an FBO:

.. code-block:: python

    # Shorcut for creating a single layer FBO with depth buffer
    fbo = FBO.create(1024, 1024, depth=True)

    # Multilayer FBO (We really need to make a shortcut for this!)
    fbo = FBO()
    fbo.add_color_attachment(texture1)
    fbo.add_color_attachment(texture2)
    fbo.add_color_attachment(texture3)
    fbo.set_depth_attachment(depth_texture)

    # Binding and releasing FBOs
    fbo.bind()
    fbo.release()

    # Using a context manager
    with fbo:
        # Draw stuff in the FBO

When binding the FBOs with multiple color attachments it will automatically
call ``glDrawBuffers`` enabling multiple outputs in the fragment shader.

Shader example with multiple layers:

.. code-block:: glsl

    #version 410

    layout(location = 0) out vec4 outColor0;
    layout(location = 1) out vec4 outColor1;
    layout(location = 2) out vec4 outColor2;

    void main( void ) {
        outColor0 = vec4(1.0, 0.0, 0.0, 1.0)
        outColor1 = vec4(0.0, 1.0, 0.0, 1.0)
        outColor1 = vec4(0.0, 0.0, 1.0, 1.0)
    }

Will draw red, green and blue in the separate layers in the FBO/textures.

.. Warning:: It's important to use explicit attribute locations as not all drivers
   will guarantee preservation of the order and things end up in the wrong buffers!

Another **very important** feature of the FBO implementation is
the concept of FBO stacks.

- The default render target is the window frame buffer.
- When the stack is empty we are rendering to the screen.
- When binding an FBO it will be pushed to the stack and the correct viewport
  for the FBO will be set
- When releasing the FBO it will be popped from the stack and
  the viewport for the default render target will be applied
- This also means we can build deeper stacks with the same behavior
- The maximum stack depth is currently 8 and the framework will
  aggressively react when FBOs are popped and pushed in the wrong order

A more complex example:

.. code-block:: python

    # Push fbo1 to stack, bind and set viewport
    fbo1.bind()
    # Push fbo2 to stack, bind and set viewport
    fbo2.bind()
    # Push fbo3 to stack, bind and set viewport
    fbo3.bind()
    # Pop fbo3 from stack, bind fbo2 and set the viewport
    fbo3.release()
    # Pop fbo2 from stack, bind fbo1 and set the viewport
    fbo2.release()
    # Pop fbo1 from stack, unbind the fbo and set the screen viewport
    fbo1.release()

Using context managers:

.. code-block:: python

    with fbo1:
        with fbo2:
            with fbo2:
                pass

This is especially useful in realation to the ``draw`` method in effects.
The last parameter is the target FBO. The effect will never know if the
FBO passed in is the fake window FBO or an actual FBO. It might also
do offscreen rendering to its own fbos and things start get get really ugly.

The FBO stack makes this fairly painless.

By using the ``bind_target`` decorator on the ``draw`` method of your effect
you will never need to think about this issue. Not having to worry about
resporting the viewport size is also a huge burden off our shoulders.

.. code-block:: python

    @effect.bind_target
    def draw(self, time, frametime, target):
        # ...

There are of course ways to bypass the stack, but should be done with extreme caution.

.. Note:: We are also aiming to support layered rendering using the geometry shader.
   Please make an issue or pull request on github.

.. autoclass:: demosys.opengl.fbo.FBO
    :members:
    :undoc-members:
    :show-inheritance:
