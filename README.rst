|pypi| |travis| |rtd|

demosys-py
==========

A python 3 implementation of a C++ project used to create and
prototype demos (see
`demoscene <https://en.wikipedia.org/wiki/Demoscene>`__) in OpenGL. The
design of this version is heavily inspired by the
`Django <https://www.djangoproject.com/>`__ project.

+-----------------+-----------------+
| |screenshot1|   | |screenshot2|   |
+-----------------+-----------------+

We only support OpenGL 3.3+ forward compatible core profiles (no backwards compatibility).

This was originally made for for non-interactive real time graphics
combined with music ("real time music videos"). It's made for people who
enjoy playing around with modern OpenGL without having to spend lots of
time creating all the tooling to get things up and running.

If you are not a fan of using a framework, you can create your own context
and just use the classes in ``demosys.opengl``. These will give you fairly
straight forward ways to use VAOs, Shaders, Textures and FBOs.

Documentation
-------------

Project documentation can be found at readthedocs_. Optionally you can
build your own docs from the ``docs`` directory.

Features
--------

- A simple effect system based on python packages
- Managment commands to create new projects and effects
- Convenient wrappers for VAO, Shader, Texture, FBO
- On-the-fly Shader and VAO negotiation of the needed buffer binding
- Strict validation in most OpenGL operations with reasonable error feedback
- Timeline / Timer support
- Support for the rocket sync-tracker system to create interesting keyframe data
- A highly pluggable framework
- Support for custom management commands
- Camera and system camera support so we can easily inspect our scene
- Easy resource management system (shaders, textures)
- Supports vertex, fragment and geometry shaders (tessellation soon (tm))
- A geometry module for quick creation of common mesh/VAO types
- Well documented (soon (tm))

Requirements
------------

In order to use the framework it's an advantage to know the following:

- Basic or intermediate Python knowledge
- Basic glsl knowledge
- Basic knowledge about matrix math

If you are missing any of these requirements, the framework can definitely be used
to learn the. Zero/0 lines of code are needed to generate a project with a spinning
cube and you can get started playing with things.

Contributing
------------

Any contribution to the project is welcome. Never hesitate to ask
questions or submit pull requests (completed or work in progress). The
worst thing that can happen is that we or you might learn something.
This is supposed to be a fun project.

Also check out the `TODO list <TODO.md>`__. Take a stab on what of the
features or documentation or suggest new entries.

Known Issues
------------

The sound player an be a bit wonky at times on startup refusing to play
on some platforms. We have tried a few libraries and ended up using
pygame's mixer module. (Optional setup for this)

Audio Requirements:

- As the current position in the music is what all
  draw timers are connected to, we need a library that can deliver this.
- Efficient and accurate seeking + pause support
- Some way to extract simple data from the music for visualisation

Libraries
---------

GLFW binaries must also be installed. Get from your favourite location.
Use version 3.2.1 or later.

-  `http://pyopengl.sourceforge.net <http://pyopengl.sourceforge.net/>`__
-  `pyGLFW <https://github.com/FlorianRhiem/pyGLFW>`__ for window and
   context creation + input
-  `PIL/Pillow <https://github.com/python-pillow/Pillow>`__ for texture
   loading
-  https://github.com/adamlwgriffiths/Pyrr for math (uses numpy)

Optional for audio:
-  https://www.pygame.org using the mixer module for music

What inspired us to make this project?
--------------------------------------

- We are old farts from the demoscene
- We love Python
- We were wondering what would be done with OpenGL in Python
- We work a lot with Django and love it

Why not combine ideas from our own demosys written in C++ and Django
making a Python 3 version?

Credits
-------

-  Also thanks to `Attila
   Toth <https://www.youtube.com/channel/UC4L3JyeL7TXQM1f3yD6iVQQ>`__
   for an excellent tutorial on OpenGL in Python.


.. _testdemo: https://github.com/Contraz/demosys-py-test
.. |pypi| image:: https://img.shields.io/pypi/v/demosys-py.svg
   :target: https://pypi.python.org/pypi/demosys-py
.. |travis| image:: https://travis-ci.org/Contraz/demosys-py.svg?branch=master
   :target: https://travis-ci.org/Contraz/demosys-py
.. |rtd| image:: https://readthedocs.org/projects/demosys-py/badge/?version=latest
   :target: http://demosys-py.readthedocs.io/en/latest/?badge=latest
.. |screenshot1| image:: https://objects.zetta.io:8443/v1/AUTH_06e2dbea5e824620b20b470197323277/contraz.no-static/gfx/productions/SimLife3.png
.. |screenshot2| image:: https://objects.zetta.io:8443/v1/AUTH_06e2dbea5e824620b20b470197323277/contraz.no-static/gfx/productions/SimLife2.png
.. _readthedocs: http://demosys-py.readthedocs.io/
