[![pypi](https://img.shields.io/pypi/v/demosys-py.svg)](https://pypi.python.org/pypi/demosys-py) [![travis](https://travis-ci.org/Contraz/demosys-py.svg?branch=master)](https://travis-ci.org/Contraz/demosys-py) [![rtd](https://readthedocs.org/projects/demosys-py/badge/?version=latest)](http://demosys-py.readthedocs.io/en/latest/?badge=latest)

demosys-py
==========

A Python 3 cross platform OpenGL 3.3+ core framework based on [ModernGL](https://github.com/cprogrammer1994/ModernGL)

![screenshot1](https://camo.githubusercontent.com/32ce052715e574ae4e6fc60384b5070cbc9aaa27/68747470733a2f2f6f626a656374732e7a657474612e696f3a383434332f76312f415554485f30366532646265613565383234363230623230623437303139373332333237372f636f6e7472617a2e6e6f2d7374617469632f6766782f70726f64756374696f6e732f53696d4c696665332e706e67) ![screenshot2](https://camo.githubusercontent.com/653387f2f7f144b29b6fb9c891a17482b089e02d/68747470733a2f2f6f626a656374732e7a657474612e696f3a383434332f76312f415554485f30366532646265613565383234363230623230623437303139373332333237372f636f6e7472617a2e6e6f2d7374617469632f6766782f70726f64756374696f6e732f53696d4c696665322e706e67)

---

Originally made for for non-interactive real time graphics combined with music
("real time music videos", see [demoscene](https://en.wikipedia.org/wiki/Demoscene))
but can of course be used almost any purpose.

Made for people who enjoy playing around with modern OpenGL without spending lots of
time creating all the tooling to get things up and running. Using [ModernGL](https://github.com/cprogrammer1994/ModernGL)
also makes working with OpenGL a breeze accomplishing a lot with very few lines of code.

A high priority for this project is also to help improving [ModernGL](https://github.com/cprogrammer1994/ModernGL).

* [Documentation](http://demosys-py.readthedocs.io/)
* [ModernGL Documentation](https://moderngl.readthedocs.io)
* [Examples](https://github.com/Contraz/demosys-py/tree/master/examples)
* [Effect Templates](https://github.com/Contraz/demosys-py/tree/master/demosys/effect_templates)
* [demosys-py on Github](https://github.com/Contraz/demosys-py)
* [demosys-py on PyPi](https://pypi.python.org/pypi/demosys-py)

Creating a project with a spinning cube can be done in less than a minute.

```bash
pip install demosys-py
demosys-admin createproject myproject
demosys-admin createeffect myproject/cube
```

Now run the effect

```bash
python manage.py runeffect myproject.cube
```

Features
--------

* A simple effect system based on python packages
* Supports most modern OpenGL features through [ModernGL](https://github.com/cprogrammer1994/ModernGL)
* Loading GLTF 2.0 and wavefront obj files/scenes
* Support for the rocket sync-tracker system to create interesting keyframe data (Using [pyrocket](https://github.com/Contraz/pyrocket))
* Management commands to create new projects and effects including the ability to make custom commands
* Runtime re-loading shader programs (press R)
* A highly pluggable framework with customizable timers, resource loaders, timelines and more
* A geometry module for quick creation of common mesh/VAO types
* Experimental audio playback support

Requirements
------------

In order to use the framework it's an advantage to know the following:

* Basic or intermediate Python
* Basic glsl
* Basic matrix math

If you are missing any of these requirements the framework can definitely be used to learn. 0 lines of code are needed to generate a project with a spinning cube and you can star poking at things.

Local Development
-----------------

Installing the project in development mode (in a virtualenv):

```bash
python setup.py develop
# PyQt5 doesn't support develop and have to manually be force-reinstalled installed after
pip install -I PyQt5
```

Running tests:

```bash
# All tests
python manage.py test

# Single tests module
python manage.py test tests/test_effect.py
```

Building docs:

```bash
pip install -r requirements-test.txt
python setup.py build_sphinx
```

Contributors
------------

* [Einar Forselv](https://github.com/einarf)
* [Arttu Tamminen](https://github.com/helgrima)
* [binaryf](https://github.com/binaryf)

Libraries
---------

* [ModernGL](https://github.com/cprogrammer1994/ModernGL) PyOpenGL replacement
* [PIL/Pillow](https://github.com/python-pillow/Pillow) for texture loading
* [Pyrrr](https://github.com/adamlwgriffiths/Pyrr) for math (uses numpy)
* [PyQt5](https://pypi.org/project/PyQt5/) is default for window/context creation (works out of the box on most platforms)

Optional:

* [pyGLFW](https://github.com/FlorianRhiem/pyGLFW) for window/context creation
* [pyglet](https://bitbucket.org/pyglet/pyglet/wiki/Home) for window/context creation (Does not work on OS X)
* [pygame](https://www.pygame.org) using the mixer module for music
* [python-vlc](https://github.com/oaubert/python-vlc) for audio playback

Mentions
--------

Also consider supporting [Read the Docs](https://readthedocs.org/sustainability/) by becoming a gold member
though a one time ($5 or more) donation for an ad-free experience.
