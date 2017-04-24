
Performance
===========

When using a high level language such as Python for real time rendering we must
be extra careful with the total time we spend in Python code every frame.
At 60 frames per second we only have 16 milliseconds to get the job done.
This is ignoring delays or blocks caused by OpenGL calls.

.. Note::

    How important performance is will of course depend on the project.
    Visualization for a scientific application doing some heavy
    calculations would probably not need to run at 60 fps.
    It's also not illegal to not care about performance.

Probably the biggest enemy to performance in python is **memory allocation**.

Try to avoid creating new objects every frame if possible. This includes
all mutable data types such as lists, sets, dicts.

Another area is updating buffer object data such as VBOs and
Textures. If these are of a fairly small size it might not be a problem,
but do not expect pure Python code to be able to efficiently feed CPU-generated data
to OpenGL. If this data comes from a library though ctypes and we
can avoid re-allocating memory for each frame we might be good,
but this is not always easy to determine and will needs testing.

Try to do as much as possible on the GPU. Use features like transform
feedback to alter buffer data and use your creativity to find efficient
solutions.

Performance in rendering is not straight forward to measure in any language.
Simply adding timers in the code will not really tell us much unless
we also query OpenGL about the performance.

We could also try to compile your project with pypy, but we have not tested this (yet).

We can also strive to do more with less. Rendering, in the end, is really just
about creating illusions.
