
Settings
========


The ``settings.py`` file must be present in your project and contains
(you guessed right!) settings for the framework. This is pretty much
identical to Django.

OPENGL
^^^^^^

Using these values you are sure it will run on all platforms. OS X only
support forward compatible core contexts. This will bump you to the
latest version you drivers support.

.. code:: python

    OPENGL = {
        "version": (4, 1),
        "profile": "core",
        "forward_compat": True,
    }

The default opengl version is 4.1. Some older systems might need
that tuned down to 3.3, but generally 4.1 is widely supported.

WINDOW
^^^^^^

Window properties. If you are using Retina display, be aware that these
values refer to the virual size. The actual buffer size will be 2 x.

.. code:: python

    WINDOW = {
        "size": (1280, 768),
        "vsync": True,
        "resizable": False,
        "fullscreen": False,
        "title": "demosys-py",
        "cursor": False,
    }

MUSIC
^^^^^

If ``MUSIC`` is defined, demosys will attempt to play. (We have only
tried mp3 files!)

.. Note:: Getting audio to work requires additional setup.

.. code:: python

    PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
    MUSIC = os.path.join(PROJECT_DIR, 'resources/music/tg2035.mp3')

TIMER
^^^^^

This is the timer class that controls time in your project.
This defaults to ``demosys.timers.Timer`` that is simply keeps
track of system time using ``glfw``.

.. code:: python

    TIMER = 'demosys.timers.Timer'

Other timers are:

- ``demosys.timers.MusicTimer`` requires ``MUSIC`` to be defined and will use the current time in an mp3.
- ``demosys.timers.RocketTimer`` is the same as the default timer, but uses uses the rocket library.
- ``demosys.timers.RocketMusicTimer`` requires ``MUSIC`` and ``ROCKET`` to be configured.

ROCKET
^^^^^^

Configuration of the pyrocket_ sync-tracker library.

- ``rps``: Number of rows per second
- ``mode``: The mode to run the rocket client
  - ``editor``: Requires a rocket editor to run so the library can connect to it
  - ``project``: Loads the project file created by the editor and plays it back
  - ``files``: Loads the binary track files genrated by the client through remote export in the editor.
- ``project_file``: The absolute path to the project file
- ``files``: The absolute path to the directory containing binary track data

.. code:: python

    ROCKET = {
        "rps": 24,
        "mode": "editor",
        "files": None,
        "project_file": None,
    }

EFFECTS
^^^^^^^

Effect packages demosys will initialize and use (Same as apps in
Django).

.. code:: python

    EFFECTS = (
        'myproject.cube',
    )

SHADER_DIRS/FINDERS
^^^^^^^^^^^^^^^^^^^

``DIRS`` contains absolute paths the ``FileSystemFinder`` will look for
shader while ``EffectDirectoriesFinder`` will look for shaders in all
registered effects in the order they were added.

The ``FileSystemFinder`` will look in all paths specified in ``SHADER_DIRS``.
All paths must be absolute (just join on ``PROJECT_DIR``). This is a good way
to add project-global shaders used by multiple effecst.

.. code:: python

    SHADER_DIRS = (
        os.path.join(PROJECT_DIR, 'resources/shaders'),
    )

    SHADER_FINDERS = (
        'demosys.core.shaderfiles.finders.FileSystemFinder',
        'demosys.core.shaderfiles.finders.EffectDirectoriesFinder',
    )

TEXTURE_DIRS/FINDERS
^^^^^^^^^^^^^^^^^^^^

Same principle as ``SHADER_DIRS`` and ``SHADER_FINDERS``.

.. code:: python

    # Hardcoded paths to shader dirs
    TEXTURE_DIRS = (
        os.path.join(PROJECT_DIR, 'resource/textures'),
    )

    # Finder classes
    TEXTURE_FINDERS = (
        'demosys.core.texturefiles.finders.FileSystemFinder',
        'demosys.core.texturefiles.finders.EffectDirectoriesFinder'
    )

SCREENSHOT_PATH
^^^^^^^^^^^^^^^

Absolute path to the directory screenshots will be saved.
If not defined or the directory don't exist, the current working directory will be used.

.. code:: python

    SCREENSHOT_PATH = os.path.join(PROJECT_DIR, 'screenshots')


.. _pyrocket: https://github.com/Contraz/pyrocket