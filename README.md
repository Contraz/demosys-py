[![pypi](https://img.shields.io/pypi/v/demosys-py.svg)](https://pypi.python.org/pypi/demosys-py) [![travis](https://travis-ci.org/Contraz/demosys-py.svg?branch=master)](https://travis-ci.org/Contraz/demosys-py) [![rtd](https://readthedocs.org/projects/demosys-py/badge/?version=latest)](http://demosys-py.readthedocs.io/en/latest/?badge=latest)

demosys-py
==========

A Python 3 cross platform modern OpenGL 3.3+ core framework based on [ModernGL](https://github.com/cprogrammer1994/ModernGL)

![screenshot1](https://camo.githubusercontent.com/32ce052715e574ae4e6fc60384b5070cbc9aaa27/68747470733a2f2f6f626a656374732e7a657474612e696f3a383434332f76312f415554485f30366532646265613565383234363230623230623437303139373332333237372f636f6e7472617a2e6e6f2d7374617469632f6766782f70726f64756374696f6e732f53696d4c696665332e706e67) ![screenshot2](https://camo.githubusercontent.com/653387f2f7f144b29b6fb9c891a17482b089e02d/68747470733a2f2f6f626a656374732e7a657474612e696f3a383434332f76312f415554485f30366532646265613565383234363230623230623437303139373332333237372f636f6e7472617a2e6e6f2d7374617469632f6766782f70726f64756374696f6e732f53696d4c696665322e706e67)

---

Originally made for for non-interactive real time graphics combined with music
("real time music videos", see [demoscene](https://en.wikipedia.org/wiki/Demoscene)
but can of course be used for other purposes.

Made for people who enjoy playing around with modern OpenGL without spending lots of time creating all the tooling to get things up and running.

* [Documentation](http://demosys-py.readthedocs.io/)
* [Examples](https://github.com/Contraz/demosys-py-test)
* [Effect Templates](https://github.com/Contraz/demosys-py/tree/master/demosys/effect_templates)
* [demosys-py on Github](https://github.com/Contraz/demosys-py)
* [demosys-py on PyPi](https://pypi.python.org/pypi/demosys-py)

Creating a project with a spinning cube can be done in less than a minute.
(Assuming you have glfw installed)

```bash
pip install demosys-py
demosys-admin createproject myproject
demosys-admin createeffect myproject/cube
```

Now edit ``myproject/settings.py`` adding the effect in ``EFFECTS``.

```python
EFFECTS = (
  'myproject.cube',  # note the comma!
)
```

Now run the effect!

```bash
./manage.py run
```

Features
--------

* A simple effect system based on python packages
* Supports loading GLTF and obj files/scenes
* Support for the rocket sync-tracker system to create interesting keyframe data (Using [pyrocket](https://github.com/Contraz/pyrocket))
* Management commands to create new projects and effects
* Convenient wrappers for VAO, Shader, Texture, FBO etc
* On-the-fly Shader and VAO negotiation of the needed buffer binding
* Runtime re-loading shaders (press R)
* Strict validation in most OpenGL operations with reasonable error feedback
* Time line / Timer support
* A highly pluggable framework
* Support for custom management commands
* Camera and system camera support so we can easily inspect our scene
* Easy resource management system (shaders, textures)
* Supports vertex, fragment and geometry shaders (tessellation is wip)
* A geometry module for quick creation of common mesh/VAO types
* (Experimental audio playback support)

Requirements
------------

In order to use the framework it's an advantage to know the following:

* Basic or intermediate Python
* Basic glsl
* Basic matrix math

If you are missing any of these requirements the framework can definitely be used to learn. 0 lines of code are needed to generate a project with a spinning cube and you can star poking at things.

Contributors
------------

* [Einar Forselv](https://github.com/einarf)
* [Arttu Tamminen](https://github.com/helgrima)

Libraries
---------

GLFW binaries must be installed. Get from your favourite location. Use version 3.2.1 or later.

* [pyGLFW](https://github.com/FlorianRhiem/pyGLFW) for window and context creation + input
* [PIL/Pillow](https://github.com/python-pillow/Pillow) for texture loading
* [Pyrrr](https://github.com/adamlwgriffiths/Pyrr) for math (uses numpy)

Optional for audio:

- [pygame](https://www.pygame.org) using the mixer module for music
