
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