# demosys-py

A python 3 implementation of a C++ project used to create and prototype
demos (see demoscene) in OpenGL. The design of this version is heavily
inspired by the Django project.

We only support OpenGL 4.1+ core profiles (no backwards compatibility).

This was originally made for for non-interactive real time graphics combined
with music ("real time music videos"). It's made for people who enjoy
playing around with modern OpenGL without having to spend lots of time
creating all the tooling to get things up and running.

Anything we draw to the screen must be implemented as an Effect.
If that effect is one or multiple things is entirely up to you.
An effect is an individual package/directory containing an `effect.py`
module. This package can also contain a `shaders` and `textures` directory
that demosys will automatically find and load resources from.

## Libraries

- Library for matrix and vector algebra: http://pyrr.readthedocs.io
- https://www.pygame.org using the mixer module

