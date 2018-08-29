
Creating Geometry
=================

In order to render something to the screen we need geometry as vertex arrays.

We have the following options:

* Using the :py:mod:`demosys.geometry` module (or extend the geometry module)
* Loading scenes/meshes from file using the supported file formats (or create new loaders of other formats)
* Generating your own geometry programmatically

The geometry module
-------------------

The ``demosys.geometry`` module currently provides some simple
functions to generate VAOs for simple things.

Examples:

.. code-block:: python

    from demosys import geometry
    # Create a fullscreen quad for overing the entire screen
    vao = geometry.quad_fs()

    # Create a 1 x 1 quad on the xy plane
    vao = geometry.quad_2f(with=1.0, height=1.0)

    # Create a unit cube
    vao = geometry.cube(1.0, 1.0, 1.0)

    # Create a bounding box
    vao = geometry.bbox()

    # Create a sphere
    vao = geometry.sphere(radius=0.5, sectors=32, rings=16)

    # Random 10.000 random points in 3d
    vao = geometry.points_random_3d(10_000)

.. Note:: Improvements or suggestions can be made by through pull
   requests or issues on github.

See the :py:mod:`demosys.geometry` reference for more info.

Scene/Mesh File Formats
-----------------------

The ``demosys.scene.loaders`` currently support loading
wavefront obj files and gltf 2.0 files.

You can create your own scene loader by adding the loader
class to ``SCENE_LOADERS``.

.. code-block:: python

    SCENE_LOADERS = (
        'demosys.scene.loaders.gltf.GLTF2',
        'demosys.scene.loaders.wavefront.ObjLoader',
    )

Generating Custom Geometry
--------------------------

To efficiently generate geometry in Python we must avoid as much memory
allocation as possible. If performance doesn't matter, then take this
section lightly.

There are many lbraries out there such as ``numpy`` capable of generating
geometry fairly efficiently. Here we mainly focus on creating it ourselves
using pure python code. We're also using the :py:class:`demosys.opengl.vao.VAO`
for vertex buffer construction. This can easily be translated into using
``moderngl.VertexArray`` directly if needed.

The naive way of generating geometry would probably look something like this:

.. code-block:: python

   import numpy
   import moderngl
   from pyrr import Vector3

   def random_points(count):
       points = []
       for p in range(count):
           # Let's pretend we calculated random values for x, y, z
           points.append(Vector3([x, y, x]))

       # Create VBO enforcing float32 values with numpy
       points_data = numpy.array(points, dtype=numpy.float32)

       vao = VAO("random_points", mode=moderngl.POINTS)
       vao.buffer(points_data, 'f4', "in_position")
       return vao

This works perfectly fine, but we allocate a new list for every iteration
and pyrr internally creates a numpy array. The ``points`` list will also
have to dynamically expand. This gets more ugly as the ``count`` value increases.

We move on to version 2:

.. code-block:: python

   def random_points(count):
       # Pre-allocate a list containing zeros of length count * 3
       points = [0] * count * 3
       # Loop count times incrementing by 3 every frame
       for p in range(0, count * 3, 3):
           # Let's pretend we calculated random values for x, y, z
           points[p] = x
           points[p + 1] = y
           points[p + 2] = z

     points_data = numpy.array(points, dtype=numpy.float32)

This version is at least and order of magnitude faster because we don't allocate memory
in the loop. It has one glaring flaw. It's **not a very pleasant read**
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

       points_data = numpy.fromiter(generate(), count=count * 3, dtype=numpy.float32)

Using generators in Python like this is much a cleaner way. We also take
advantage of numpy's ``fromiter()`` that basically slurps up all the
numbers we yield into its internal buffers. By also telling
numpy what the final size of the buffer will be using the ``count``
parameter, it will pre-allocate this not having to dynamically increase
its internal buffer.

Generators are extremely simple and powerful. If things get complex we can
easily split things up in several functions because Python's ``yield from``
can forward generators.

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

       interleaved_data = numpy.fromiter(generate(), count=count * 8, dtype=numpy.float32)
