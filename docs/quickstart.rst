
Getting Started
===============

Make sure you have Python 3.5 or later installed. On Windows and OS X you can
simply install the latest Python 3 by downloading an installer from the
`Official Python site <https://www.python.org/>`_.

Create a virtualenv
^^^^^^^^^^^^^^^^^^^

First of all create a directory for your project and navigate to it using a
terminal. We assume Python 3.6 here.

OS X / Linux

.. code-block:: shell

    python3.6 -m pip install virtualenv
    python3.6 -m virtualenv env
    source env/bin/activate

Windows

.. code-block:: shell

    python36.exe -m pip install virtualenv
    python36.exe -m virtualenv env
    .\env\Scripts\activate

We have now created and activated an isolated Python environment and are
ready to install packages without affecting the Python versions in our
operating system.

Setting up a Project
^^^^^^^^^^^^^^^^^^^^

Install the demosys-py

.. code-block:: shell

    pip install demosys-py

This will add a new command ``demosys-admin`` we use to create a project.

.. code-block:: shell

    demosys-admin createproject myproject

This will generate the following files:

.. code-block:: bash

    myproject
    └── settings.py
    └── project.py
    manage.py

- ``settings.py``: the settings for your project
- ``project.py``: your project config
- ``manage.py``: entrypoint script for running your project

These files can be left unchanged for now. We mainly need ``manage.py``
as an entrypoint to the framework and the default ``settings`` should be enough.

- An overview of the settings can be found in the :doc:`/reference/settings` section.
- More information about projects can be found in the :doc:`/user_guide/project` section.


Creating an Effect Package
^^^^^^^^^^^^^^^^^^^^^^^^^^

In order to draw something to the screen we have to make an effect package
with at least one effect. We can create this effect package in the root
or inside ``myproject``. Since we don't care about project (yet), we
create it in the root.

.. code-block:: bash

    demosys-admin createeffect cube

We should now have the following structure:

.. code-block:: shell

    cube
    ├── effects.py
    ├── dependencies.py
    └── resources
        └── programs
            └── cube
                └── default.glsl

The ``cube`` directory is a copy of the deault effect pacakge template:

- The ``effects.py`` module containing one or multiple :py:class:`demosys.effects.Effect` implementation
- A ``dependencies.py`` module describing effect package dependencies and resources for this package
- A local ``resources/programs`` directory for glsl shader programs specific to the effect

dependencies.py::

    from demosys.resources.meta import ProgramDescription

    # We don't depend on any other effect packages at the moment
    effect_packages = []

    # We tell the system to load our shader program storing it with label "cube_plain".
    # The shader program can then be obtained in the effect instance using this label.
    resources = [
        ProgramDescription(label='cube_plain', path='cube_plain.glsl'),
    ]

Other resource types are also supported such as textures, programs, scenes/meshes
and miscellaneous data types. More on this in the :doc:`/user_guide/resources` section.

Also take a minute to look through the ``effects.py`` module. It contains a fair amount
of comments what will explain things. This should be very recognizalbe if you have worked
with OpenGL.

.. Note::

    Notice the ``programs`` directory also has a sub-folder
    with the same name as the effect package. This is because these directories are added
    to a search path for all programs and the only way to make these resources unique
    is to put them in a directory.

We can now run the effect that shows a spinning cube

.. code-block:: bash

    python manage.py runeffect cube

Effect packages can be reusable between projects and can also potentially be shared with
others as python packages in private repos or on `Python Package Index <http://test.org>`_.
