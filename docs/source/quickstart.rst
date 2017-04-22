
Getting Started
===============

Python 3
^^^^^^^^

Make sure you have Python 3 installed. On Windows and OS X you can simply install
the latest Python 3 by downloading an installer from the official_ Python site.

.. Note:: We recommend Python 3.6 or higher because of general **speed improvements**
    of the language, but Python versions down to 3.4 should work.

Most linux distributions already have at least Python 3.4 installed thought ``python3``.
See documentation for your distribution on how to install a newer versions.

It is common to have multiple versions of Python installed on all operating systems.

Binary Dependencies
^^^^^^^^^^^^^^^^^^^

We use glfw_ for creating an OpenGL context, windows and handling keyboard and mouse events.
This is done thought the pyGLFW_ package that is a ``ctype`` wrapper over the origonal GLFW
api. You will have to install the actual library yourself.

We require glfw 3.2.1 or later.

**OS X**

    brew install gflw

**Linux**

glfw should be present in the vast majority of the package managers.

**Windows**

Download binaries from the glfw_ website.

We do also support audio playback that will need additional dependencies, but this
is covered in a different section.

Create a virualenv
^^^^^^^^^^^^^^^^^^

First of all create a directory for your project and navigate to it using a terminal.
We assume Python 3.6 here.

OS X / Linux

.. code-block:: bash

    python3.6 -m pip install virtualenv
    python3.6 -m virtualenv env
    source env/bin/activate

Windows

.. code-block:: shell

    python36.exe -m pip install virtualenv
    python36.exe -m virtualenv env
    \env\Scripts\activate

We have now created an isolated Python environment and are ready to install packages
without affecting the Python version in our operating system.

Setting up a Project
^^^^^^^^^^^^^^^^^^^^

First of all, install the package (you should already be inside a virtualenv)

    pip install demosys-py

The package will add a new command ``demosys-admin`` we will now use to create a project.

    demosys-admin createproject myproject

This will generate the following files:

.. code-block:: bash

    myproject
    └── settings.py
    manage.py

- ``settings.py`` is the settings for your project
- ``manage.py`` is an executable script for running your project

In order to get something to the screen we have to make an effect.

.. code-block:: bash

    cd myproject
    demosys-admin createeffect cube

We should now have the folloing structure:

.. code-block:: bash

    myproject/
    ├── cube
    │   ├── effect.py
    │   ├── shaders
    │   │   └── cube
    │   │       └── default.glsl
    │   └── textures
    │       └── cube
    └── settings.py
    manage.py

The ``cube`` directory is a template for an effect:
- The standard ``effect.py`` module containing a single ``Effect`` implementation
- A local ``shaders`` directory for glsl shaders specific to the effect
- A local ``textures`` directory for texture files specific to the effect

Notice that the ``shaders`` and ``textures`` directory also has a sub-folder with the same name
as the effect. This is because these directories are added to a global virtual directory
and the only way to make these resources unique is to put it in a directory that is *hopefully* unique.

This can of course be used in creative ways to also override resources on purpose.

For the effect to be recognized by the system we need to add it ``EFFECTS`` in
``settings.py``.

.. code-block:: bash

    EFFECTS = (
        'myproject.cube',  # Remember comma!
    )

As you can see, effects are added by using the python package path. Where you put effect
packages is entirely up to you, but a safe start is to put them inside the project
package as this removes any possibility of effect package names colliding with other
python packages.

We can now run the effect that shows a spinning cube!

.. code-block:: bash

    ./manage.py runeffect myproject.cube

.. _official: https://www.python.org/
.. _glfw: http://www.glfw.org/
.. _pyGLFW: https://github.com/FlorianRhiem/pyGLFW
