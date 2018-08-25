
Project
=======

Before we can do anything with the framework we need to create a project.
A project is simply a package containing a ``settings.py`` module
and a ``manage.py`` entrypoint script.
This is also required to run effect packages using ``runeffect``.

This can be auto-generated using the ``demosys-admin`` command:

.. code:: shell

    demosys-admin createproject myproject

This will generate the following structure:

.. code-block:: shell

    myproject
    └── settings.py
    manage.py
    project.py

- ``settings.py`` is the settings for your project with good defaults. See
  :doc:`/settings` for more info.
- ``manage.py`` is the entrypoint for running your project
- ``project.py`` is used to initialize more complex project.

The project.py Module
---------------------

The ``project.py`` module is the standard location to configure more complex projects.
We achieve this by creating a class implementing :py:class:`BaseProject`.
This class contains references to all resources, effect packages, effect instances
and whatnot so we can freely configure our project::

    from demosys.project.base import BaseProject

    class Project(BaseProject):
        effect_packages = [
            'myproject.cube',
        ]
        resources = []

        def create_effect_instances(self):
            # Create three instances of a cube effect that takes a color keyword argument
            # adding them to the internal effect instance dictionary using label as the key
            # Args: label, class name, arguments to effect initializer
            self.create_effect('cube_red', 'CubeEffect', color=(1.0, 0.0, 0.0))
            self.create_effect('cube_green', 'CubeEffect', color=(0.0, 1.0, 0.0))
            # Use full path to class
            self.create_effect('cube_blue', 'myproject.cube.CubeEffect', color=(0.0, 0.0, 1.0))

This project configuration is used when the ``run`` command is issued.
For the project class to be recognized we need to update the ``settings.PROJECT``
attribute with the python path::

    PROJECT = 'myproject.project.Project'

``manage.py run`` will now run the project using this project configuration.

How you organize your resources and effects are entirely up to you. You can
load all resources in the Project class and/or have effect packages loading
their own resources. Resources dependencies for effect packages are always
loaded automatically when adding the package to ``effect_packages``
(can be overriden by implementing the ``create_external_resources`` method.

The Project class also have direct access to the moderngl context
through ``self.ctx``, so you are free to manually create any global
resource (like framebuffers) and assign them to effects.

The created effect instances can then be used by a timeline class deciding what
effects should be rendered at any given point in time.
The default timeline configured just grabs the first runnable effect it finds and render only that one.

Timers
------

Timers are classes responsible for controlling the current time.
It simply reports the number of seconds as a float since effect rendering started.
Timers also need to support pausing and time seeking so we can
freely move around in the timeline. 

This time value is passed through the configured timeline class and forwarded
to each active effect through their ```draw()`` method.
We should assume time can move in any direction at any speed and suddenly
jump forward and backwards in time.

The default timer if not specified in settings:

.. code-block:: shell

    TIMER = 'demosys.timers.clock.Timer'

Standard Timers
^^^^^^^^^^^^^^^

- :py:class:`demosys.timers.clock.Timer`: Default timer just tracking time in seconds using pythons ``time`` module.
- :py:class:`demosys.timers.music.Timer`: Timer playing music reporting duration in the song
- :py:class:`demosys.timers.rocket.Timer`: Timer using the rocket sync system
- :py:class:`demosys.timers.rocketmusic.Timer`: Timer using the rocket sync system with
  music playback

You create a custom timer by extending :py:class:`demosys.timers.base.BaseTimer`.

Timelines
---------

A timeline is a project responsible for knowing exactly when an effect instance
is active based on the reported time from a timer.

The current standard timelines are:

* :py:class:`demosys.timeline.single.Timeline`: Grabs a the single effect instance from your project rendering it
* :py:class:`demosys.timeline.rocket.Timeline`: The active status of each effect is decided by rocket

New timeline classes can be created by extending :py:class:`demosys.timeline.base.BaseTimeline`.

Effects Package Organization
----------------------------

By default it's a good idea to put effect packages inside the project package as
this protects you from package name collisions and makes distribution of the
project through `Python Package Index <https://pypi.org/>`_ simpler.

An exeption is when creating a reusable effect package in a separate repository.
The effect package could for example be named ``demosys_postprocessing``
containing configurable effects doing various postprocessing techniques.

.. Note:: We encourage you to share reusable effect packages on `pypi <https://pypi.org/>`_
          and are planning add these links these in the project description on github.
          (Make an issue or PR)

manage.py
---------

The ``manage.py`` script is an alternative entry point to ``demosys-admin``
that properly setting the ``DEMOSYS_SETTINGS_MODULE`` enviroment variable
for your project. The main purpose of ``demosys-admin`` is to initially have an entry point
to the commands creating a projects when we don't have a ``manage.py`` yet.

By default ``manage.py`` sets your settings module to ``<project_name>.settings``
matching the default auto generated settings module. You can override this
by setting the ``DEMOSYS_SETTINGS_MODULE`` enviroment variable before
running ``manage.py``.

Examples of ``manage.py`` usage:

.. code-block:: shell

    # Create a new project
    python manage.py createproject myproject

    # Create effect inside a project
    python manage.py createeffect myproject/myeffect

    # Run a specific effect package
    python manage.py runeffect myproject.myeffectpackage

    # Run using the ``project.py`` configuration.
    python manage.py run

    # Run a cusom command
    python manage.py <custom command> <custom arguments>

The ``manage.py`` script is executable by default and can be executed directly
``./manage.py <arguments>`` on linux and OS X. 

Effect Templates
----------------

A collection of effect templates reside in ``effect_templates`` directory.
To list the available templates:

.. code-block:: shell

    $ ./manage.py createeffect --template list
    Available templates: cube_simple, empty, raymarching_simple

To create a new effect with a specific template

.. code-block:: shell

    $ ./manage.py createeffect myproject/myeffect --template raymarching_simple

.. Note::

    If you find the current effect templates insufficent
    please make a pull request or report the issue on github.

Management Commands
-------------------

Custom commands can be added to your project. This can be useful when you need
additional tooling or whatever you could imagine would be useful to run from
``manage.py``.

Creating a new command is fairly straight forward. Inside your project package,
create the ``management/commands/`` directories. Inside the commands directory
we can add commands. Let's add the command ``convert_meshes``.

The project structure (excluding effects) would look something like:

.. code-block:: shell

    myproject
    └── management
        └── commands
            └── convert_meshes.py

Notice we added a ``convert_meshes`` module inside ``commands``. The name of the module
will be name of the command. We can reach it by:

.. code-block:: shell

    ./manage.py convert_meshes

Our test command would look like this:

.. code-block:: shell

    from demosys.core.management.base import BaseCommand

    class Command(BaseCommand):
        help = "Converts meshes to a more desired format"

        def add_arguments(self, parser):
            parser.add_argument("message", help="A message")

        def handle(self, *args, **options):
            print("The message was:", options['message'])

- ``add_arguments`` exposes a standard argparser we can add arguments for the
  command.
- ``handle`` is the actual command logic were the parsed arguments are passed
  in
- If the parameters to the command do not meet the requirements for the parser,
  a standard arparse help will be printed to the terminal
- The command class must be named ``Command`` and there can only be one command
  per module

The idea is to create modules doing the actual command work in the ``management``
package while the command modules deal with the basic input/output.