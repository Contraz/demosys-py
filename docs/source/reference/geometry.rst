geometry
========

The geometry module is a collection of functions
generating simple geometry / VAOs.

.. py:module:: demosys.geometry
.. py:currentmodule:: demosys.geometry

Functions
---------

.. autofunction:: quad_fs() -> VAO
.. autofunction:: quad_2d(width, height, xpos=0.0, ypos=0.0) -> VAO
.. autofunction:: cube(width, height, depth, normals=True, uvs=True) -> VAO
.. autofunction:: bbox(width=1.0, height=1.0, depth=1.0) -> VAO
.. autofunction:: plane_xz(size=(10, 10), resolution=(10, 10)) -> VAO
.. autofunction:: points_random_3d(count, range_x=(-10.0, 10.0), range_y=(-10.0, 10.0), range_z=(-10.0, 10.0), seed=None) -> VAO
.. autofunction:: sphere(radius=0.5, sectors=32, rings=16) -> VAO
