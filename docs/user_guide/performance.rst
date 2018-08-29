
Performance
===========

When using a high level language such as Python for real time rendering we must
be extra careful with the total time we spend in Python code every frame.
At 60 frames per second we only have 16 milliseconds to get the job done.
This is ignoring delays or blocks caused by OpenGL calls.

.. Note::

    How important performance is will of course depend on the project.
    Visualization for a scientific application doing some heavy
    calculations would probably not need to run at 60+ fps.
    It's also not illegal to not care about performance.

Your Worst Enemy: Memory Allocation
-----------------------------------

Probably the biggest enemy to performance in python is **memory allocation**.
Try to avoid creating new objects when possible.

Try to do as much as possible on the GPU. Tru to use features like
transform feedbacks, instancing and indirect rendering. Use your creativity to
find efficient solutions.

When doing many draw calls, do as little as possible between those
draw calls. Doing matrix math in python with numpy or pyrr
is **extremely slow** in the scope of real time rendering.
Try to calculate matrixes ahead of time. Also
moving the matrix calculations inside the shader programs can
help greatly.

You can easily do 1000 draw calls of a small to medium vertex array
and still run 60+ fps even on older hardware. The minute
you throw in some matrix calculation in that loop you might
be able to draw 50 before the framerate tanks.

This can also be solved by using more efficient libraries.
`miniglm <https://github.com/cprogrammer1994/miniglm>`_. have
been one suggestion that looks promising.

Conclusion
----------

Performance in rendering is not straight forward to measure in any language.
Simply adding timers in the code will not really tell us much unless
we also query OpenGL about the performance.

ModernGL have tools like ``Query`` and ``ConditionalRender`` that
can be very helpful in measuring and improving performance.
See the `ModernGL documentation <https://moderngl.readthedocs.io/en/stable/>`_
for more info.

We can also strive to do more with less. Rendering, in the end, is really just
about creating illusions. Still, it's quite amazing what can be achieved
with OpenGL and Python today when using the right tools and methods.
