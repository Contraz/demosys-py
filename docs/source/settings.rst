
Settings
========


The ``settings.py`` file must be present in your project and contains
(you guessed right!) settings for the framework. This is pretty much
identical to Django.

When running your project with ``manage.py``, the script will set
the ``DEMOSYS_SETTINGS_MODULE`` environment variable. This tells
the framework where it can import its settings from. If the environment
variable is not set, the framework cannot start.

OPENGL
^^^^^^

Using these values you are sure it will run on all platforms. OS X only
supports forward compatible core contexts. This will ensure deprecation
older features.

**We cannot guarantee that the framework will work properly for non-default values,
and you should assume severe a performance hit.**

.. code:: python

    OPENGL = {
        "version": (4, 1),  # 3.3 -> 4.1 is acceptable
        "profile": "core",
        "forward_compat": True,
    }

- ``version`` describes the major and minor version of the OpenGL context we are creating
- ``profile`` should ideally always be ``core``, but we leave it configurable for
  those who might want to include legacy OpenGL code permanently or temporary. Do note that
  not using core profile will exclude the project from working on certain setups and may
  have unexpected side effects.
- ``forward_compat`` True, is required for the project to work on OS X

The default opengl version is 4.1. Some older systems might need that tuned down to 3.3,
but generally 4.1 is widely supported. To make your project work on OS X you cannot move
past version 4.1 (sadly). This doesn't mean we cannot move past 4.1, but as of right now
we focus on implementing features up to 4.1.

WINDOW
^^^^^^

Window properties. If you are using Retina display, be aware that these
values refer to the virual size. The actual buffer size will be 2 x.

.. code:: python

    WINDOW = {
        "size": (1280, 768),
        "fullscreen": False,
        "resizable": False,
        "vsync": True,
        "title": "demosys-py",
        "cursor": False,
    }

- ``size``: The window size to open. Note that on 4k displays and retina the actual
  frame buffer size will normally be twice as large. Internally we query glfw for
  the actual buffer size so the viewport can be correctly applied.
- ``fullscreen``: True if you want to create a context in fullscreen mode
- ``resizable``: If the window should be resizable. This only applies in windowed mode.
  Currently we constrain the window size to the aspect ratio of the resolution (needs improvement)
- ``vsync``: Only render one frame per screen refresh
- ``title``: The visible title on the window in windowed mode
- ``cursor``: Should the mouse cursor be visble on the screen? Disabling
  this is also useful in windowed mode when controlling the camera on some platforms
  as moving the mouse outside the window can cause issues.

The created window frame buffer will by default use:

- RGBA8
- 32 bit depth buffer were 24 bits is for depth and 8 bits for stencil
- Double buffering
- color, depth and stencil is cleared every frame

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

EFFECT_MANAGER
^^^^^^^^^^^^^^

Effect mangers are pluggable classed that initialize and run effect.
when only having a single effect we can run it using ``runeffect``,
but when having multiple effects we need something to decide what
effect should be active.

The default effect manager is the ``SingleEffectManager`` that is
also enforced when running ``./manage.py runeffect <name>``.
If we use the ``run`` sub-command, the first registered effect will run.

.. code:: python

    EFFECT_MANAGER = 'demosys.effects.managers.single.SingleEffectManager'

More effect managers will be added to framework soon.
Read the detailed section about effect mangers for more info.

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