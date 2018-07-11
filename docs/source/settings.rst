
Settings
========

The ``settings.py`` file must be present in your project containing settings
for the project.

When running your project with ``manage.py``, the script will set
the ``DEMOSYS_SETTINGS_MODULE`` environment variable. This tells
the framework where it can import the project settings. If the environment
variable is not set, the project cannot start.

OPENGL
------

Sets the minimum required OpenGL version to run your project.
A forward compatible core context will be always be created. This means
the system will pick the highest available OpenGL version available.

The default and lowest OpenGL version is 3.3 to support a wider
range of hardware.
To make your project work on OS X you cannot move past version 4.1 (sadly).

.. code:: python

    OPENGL = {
        "version": (3, 3),
    }

Only increase the OpenGL version if you use features above 3.3.

WINDOW
------

Window/screen properties. If you are using Retina or 4k displays, be aware that
these values can refer to the virtual size. The actual buffer size will be
larger (buffer size will nomally be 2 x the window size)

.. code:: python

    WINDOW = {
        "size": (1280, 768),
        "aspect_ratio": 16 / 9,
        "fullscreen": False,
        "resizable": False,
        "vsync": True,
        "title": "demosys-py",
        "cursor": False,
    }

- ``size``: The window size to open. Note that on 4k displays and retina the
  actual frame buffer size will normally be twice as large. Internally we
  query glfw for the actual buffer size so the viewport can be correctly
  applied.
- ``aspect_ratio`` is the enforced aspect ratio of the viewport.
- ``fullscreen``: True if you want to create a context in fullscreen mode
- ``resizable``: If the window should be resizable. This only applies in
  windowed mode. Currently we constrain the window size to the aspect ratio
  of the resolution (needs improvement)
- ``vsync``: Only render one frame per screen refresh
- ``title``: The visible title on the window in windowed mode
- ``cursor``: Should the mouse cursor be visible on the screen? Disabling
  this is also useful in windowed mode when controlling the camera on some
  platforms as moving the mouse outside the window can cause issues.

The created window frame buffer will by default use:

- RGBA8 (32 bit per pixel)
- 24 bit depth buffer
- Double buffering
- color and depth buffer is cleared for every frame

MUSIC
-----

The ``MUSIC`` attribute is used by timers supporting audio playback.
When using a timer not requiring an audio file, the value is ignored.
Should contain a string with the absolute path to the audio file.

.. Note:: Getting audio to work requires additional setup.
   See the :doc:`/guides/audio` section.

.. code:: python

    PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
    MUSIC = os.path.join(PROJECT_DIR, 'resources/music/tg2035.mp3')

TIMER
-----

This is the timer class that controls time in your project.
This defaults to ``demosys.timers.Timer`` that is simply keeps
track of system time using ``glfw``.

.. code:: python

    TIMER = 'demosys.timers.Timer'

Other timers are:

- ``demosys.timers.MusicTimer`` requires ``MUSIC`` to be defined and will
  use the current time in an audio file.
- ``demosys.timers.RocketTimer`` is the same as the default timer, but uses
  the pyrocket library with options to connect to an external sync tracker.
- ``demosys.timers.RocketMusicTimer`` requires ``MUSIC`` and ``ROCKET`` to
  be configured.

More information can be found in the :doc:`/guides/timers` section.

ROCKET
------

Configuration of the pyrocket_ sync-tracker library.

- ``rps``: Number of rows per second
- ``mode``: The mode to run the rocket client

  - ``editor``: Requires a rocket editor to run so the library can
    connect to it
  - ``project``: Loads the project file created by the editor and plays it back
  - ``files``: Loads the binary track files genrated by the client through
    remote export in the editor

- ``project_file``: The absolute path to the project file (xml file)
- ``files``: The absolute path to the directory containing binary track data

.. code:: python

    ROCKET = {
        "rps": 24,
        "mode": "editor",
        "files": None,
        "project_file": None,
    }

EFFECTS
-------

Effect packages that will be recognized by the project.
Initialization should happens in the order they appear in the list.

.. code:: python

    EFFECTS = (
        'myproject.cube',
    )

EFFECT_MANAGER
--------------

Effect mangers are pluggable classed that initialize and run effects.
When only having a single effect we can run it using ``runeffect``,
but when having multiple effects we need something to decide what
effect should be active.

The default effect manager is the ``SingleEffectManager`` that is
also enforced when running ``./manage.py runeffect <name>``.
If we use the ``run`` sub-command, the first registered effect will run.

.. code:: python

    EFFECT_MANAGER = 'demosys.effects.managers.single.SingleEffectManager'

More info in the :doc:`guides/effectmanagers` section.

SHADER_STRICT_VALIDATION
------------------------

Boolean value. If ``True`` shaders will raise ``ShaderError`` when
setting uniforms variables that don't exist.

If the value is ``False`` an error message will be generated instead.

This is useful when working with shaders. Sometimes you want to allow
missing or incorrect uniforms. Other times you want to know in a more
brutal way that something is wrong.

SHADER_DIRS/FINDERS
-------------------

``SHADER_DIRS`` contains absolute paths the ``FileSystemFinder`` will
look for shaders.

``EffectDirectoriesFinder`` will look for shaders in all registered effects
in the order they were added. This assumes you have a ``shaders`` directory in
your effect package.

.. code:: python

    # Register a project-global shader directory
    SHADER_DIRS = (
        os.path.join(PROJECT_DIR, 'resources/shaders'),
    )

    # This is the defaults is the property is not defined
    SHADER_FINDERS = (
        'demosys.core.shaderfiles.finders.FileSystemFinder',
        'demosys.core.shaderfiles.finders.EffectDirectoriesFinder',
    )

TEXTURE_DIRS/FINDERS
--------------------

Same principle as ``SHADER_DIRS`` and ``SHADER_FINDERS``.
The ``EffectDirectoriesFinder`` will look for a ``textures`` directory in effects.

.. code:: python

    # Absolute path to a project-global texture directory
    TEXTURE_DIRS = (
        os.path.join(PROJECT_DIR, 'resources/textures'),
    )

    # Finder classes
    TEXTURE_FINDERS = (
        'demosys.core.texturefiles.finders.FileSystemFinder',
        'demosys.core.texturefiles.finders.EffectDirectoriesFinder'
    )

SCENE_DIRS/FINDERS
------------------

Same principle as ``SHADER_DIRS`` and ``SHADER_FINDERS``.
This is where scene files such as wavefront and gltf files are loaded from.
The ``EffectDirectoriesFinder`` will look for a ``scenes`` directory

.. code:: python

    # Absolute path to a project-global scene directory
    SCENE_DIRS = (
        os.path.join(PROJECT_DIR, 'resources/scenes'),
    )

    # Finder classes
    SCENE_FINDERS = (
        'demosys.core.scenefiles.finders.FileSystemFinder',
        'demosys.core.scenefiles.finders.EffectDirectoriesFinder'
    )


SCREENSHOT_PATH
---------------

Absolute path to the directory screenshots will be saved.
If not defined or the directory don't exist it will be created.

.. code:: python

    SCREENSHOT_PATH = os.path.join(PROJECT_DIR, 'screenshots')


.. _pyrocket: https://github.com/Contraz/pyrocket
