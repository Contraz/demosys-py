
Geometry
========

The ``demosys.opengl.geometry`` module currently provides some simple functions to generate VAOs.

- Quad: Full screen quads for drawing offscreen buffers
- Cube: Cube with normals, uvs and texture coordinates
- Plane: A plane with a dimension and resolution
- Points: Random points in 3D

.. Nore:: We definitely need more here. Please make pull requests or make an issue on github.

Creating Custom Geometry
^^^^^^^^^^^^^^^^^^^^^^^^

To efficiently generate geometry in Python we must avoid as much memory allocation as possible.
As mentioned in other sections we use PyOpenGL's VBO class that takes numpy arrays.
We also use pyrr for vector and matrix math and representation.

.. Note:: This is a "best practices" guide to efficiently generate geometry
   with python code that will scale well even for large amounts of data.
   This was benchmarked generating various vertex formats with 1M vertices.
   For fairly small data sizes doesn't matter that much.

The naive way to generate geometry would probably look something like this:

.. code-block:: python

   from OpenGL import GL
   from OpenGL.arrays.vbo import VBO
   import numpy
   from pyrr import Vector3

   def random_points(count):
       points = []
       for p in range(count):
           # Let's pretend we calculated random values for x, y, z
           points.append(Vector3([x, y, x]))

       # Create VBO enforcing float32 values with numpy
       points_vbo = VBO(numpy.array(points, dtype=numpy.float32))

       vao = VAO("random_points", mode=GL.GL_POINTS)
       vao.map_array_buffer(GL.GL_FLOAT, points_vbo)
       vao.map_buffer(points_vbo, "in_position", 3))
       vao.build()
       return vao

This works perfectly fine, but we allocate a new list for every iteration
and pyrr internally creates a numpy array of this. The ``points`` list will also
have to dynamically expand. This exponentially more ugly as the ``count``
value increases.

We move on to version 2:

.. code-block:: python

   def random_points(count):
       # Pre-allocate a list containing zeros of length count
       # We multiply by 3 to make room for a x, y and z value
       points = [0] * count * 3
       # Loop count time incrementing by 3 every frame
       for p in range(0, count * 3, 3):
           # Let's pretend we calculated random values for x, y, z
           points[p] = x
           points[p + 1] = y
           points[p + 2] = z

     points_vbo = VBO(numpy.array(points, dtype=numpy.float32))

This version is orders of magnitude faster because we don't allocate memory
in the loop. It has one glaring flaw though. It's not a very pleasant read
even for such simple task, and it will not get any better if we add more complexity.

Let's move on to version 3:

.. code-block:: python

   def random_points(count):
       def generate():
           for p in range(count):
               # Let's pretend we calculated random values for x, y, z
               yield x
               yield y
               yield z

       points_vbo = VBO(numpy.fromiter(generate(), count=count * 3, dtype=numpy.float32)

Using generators in python like this is much cleaner way. We also take advantage
of numpy's ``fromiter()`` that basically slurps up all the numbers we emit with
yield into its internal buffers. By also telling numpy what the final size of the
buffer will be using the ``count`` parameter, it will pre-allocate this not having
to dynamically increase it's internal buffer.

Generators are extremely simple and powerful. If things get complex we can easily
split things up in several functions because Pythons ``yield from`` can forward
generators.

Imagine generating a single VBO with interleaved position, normal and uv data:

.. code-block:: python

   def generate_stuff(count):
       # Returns a distorted position of x, y, z
       def pos(x, y, z):
           # Calculate..
           yield x
           yield y
           yield x

       def normal(x, y, z):
           # Calculate
           yield x
           yield y
           yield z

       def uv(x, y, x):
           # Calculate
           yield u
           yield v

       def generate(count):
           for i in range(count):
               # resolve current x, y, z pos
               yield from pos(x, y, z)
               yield from normal(x, y, z)
               yield from uv(x, y, z)

       interleaved_vbo = VBO(numpy.fromiter(generate(), count=count * 3, dtype=numpy.float32)


The geometry Module
^^^^^^^^^^^^^^^^^^^

.. automodule:: demosys.opengl.geometry.cube
    :members:
    :undoc-members:
    :show-inheritance:


.. automodule:: demosys.opengl.geometry.plane
    :members:
    :undoc-members:
    :show-inheritance:


.. automodule:: demosys.opengl.geometry.points
    :members:
    :undoc-members:
    :show-inheritance:


.. automodule:: demosys.opengl.geometry.quad
    :members:
    :undoc-members:
    :show-inheritance:
