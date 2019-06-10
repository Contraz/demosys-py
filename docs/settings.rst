
Settings
========

The ``settings.py`` file must be present in your project in order to
run the framework.

When running your project with ``manage.py``, the script will set
the ``DEMOSYS_SETTINGS_MODULE`` environment variable. This tells
the framework where it can import the project settings. If the environment
variable is not set, the project cannot start.

OPENGL
------

Sets the minimum required OpenGL version to run your project.
A forward compatible core context will be always be requested. This means
the system will pick the highest available OpenGL version available.

The default and lowest OpenGL version is 3.3 to support a wider
range of hardware.

.. Note:: To make your project work on OS X you cannot move past version 4.1.

.. code:: python

    OPENGL = {
        "version": (3, 3),
    }

Only increase the OpenGL version if you use features above 3.3.

WINDOW
------

Window/screen properties. Most importantly the ``class`` attribute
decides what class should be used to handle the window.

The currently supported classes are:

- ``demosys.context.pyqt.Window`` PyQt5 window (default)
- ``demosys.context.glfw.Window`` pyGLFW window
- ``demosys.context.pyglet.Window`` Pyglet window (Not for OS X)
- ``demosys.context.sdl2.Window`` PySDL2 window
- ``demosys.context.headless.Window`` Headless window

.. code:: python

    WINDOW = {
        "class": "demosys.context.pyqt.Window",
        "size": (1280, 768),
        "aspect_ratio": 16 / 9,
        "fullscreen": False,
        "resizable": False,
        "vsync": True,
        "title": "demosys-py",
        "cursor": False,
    }

Other Properties:

- ``size``: The window size to open.
- ``aspect_ratio`` is the enforced aspect ratio of the viewport.
- ``fullscreen``: True if you want to create a context in fullscreen mode
- ``resizable``: If the window should be resizable. This only applies in
  windowed mode.
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

SCREENSHOT_PATH
---------------

Absolute path to the directory screenshots will be saved.
Screenshots will end up in the project root of not defined.
If a path is configured, the directory will be auto-created.

.. code:: python

    SCREENSHOT_PATH = os.path.join(PROJECT_DIR, 'screenshots')

MUSIC
-----

The ``MUSIC`` attribute is used by timers supporting audio playback.
When using a timer not requiring an audio file, the value is ignored.
Should contain a string with the absolute path to the audio file.

.. Note:: Getting audio to work requires additional setup.
   See the :doc:`/guides/audio` section.

.. code:: python

    MUSIC = os.path.join(PROJECT_DIR, 'resources/music/tg2035.mp3')

TIMER
-----

This is the timer class that controls the current time in your project.
This defaults to ``demosys.timers.clock.Timer`` that is simply keeps
track of system time.

.. code:: python

    TIMER = 'demosys.timers.clock.Timer'

Other timers are:

- ``demosys.timers.MusicTimer`` requires ``MUSIC`` to be defined and will
  use the current time in an audio file.
- ``demosys.timers.RocketTimer`` is the same as the default timer, but uses
  the pyrocket library with options to connect to an external sync tracker.
- ``demosys.timers.RocketMusicTimer`` requires ``MUSIC`` and ``ROCKET`` to
  be configured.

Custom timers can be created.
More information can be found in the :doc:`/user_guide/timers` section.


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


TIMELINE
--------

A timeline is a class deciding what effect(s) should be rendered
(including order) at any given point in time.

.. code:: python

    # Default timeline only rendeing a single effect at all times
    TIMELINE = 'demosys.timeline.single.Timeline'

You can create your own class handling this logic.
More info in the :doc:`/user_guide/timeline` section.

PROGRAM_DIRS/PROGRAM_FINDERS
----------------------------

``PROGRAM_DIRS`` contains absolute paths the ``FileSystemFinder`` will
look for shaders programs.

``EffectDirectoriesFinder`` will look for programs in all registered effect packages
in the order they were added. This assumes you have a ``resources/programs`` directory in
your effect packages.

A resource can have the same path in multiple locations. The system will return
the last occurance of the resource. This way it is possible to override resources.

.. code:: python

    # This is the defaults is the property is not defined
    PROGRAM_FINDERS = (
        'demosys.core.programfiles.finders.FileSystemFinder',
        'demosys.core.programfiles.finders.EffectDirectoriesFinder',
    )

    # Register a project-global programs directory
    # These paths are searched last
    PROGRAM_DIRS = (
        os.path.join(PROJECT_DIR, 'resources/programs'),
    )

``PROGRAM_DIRS`` can really be any directory and doesn't need to end with ``/programs``

PROGRAM_LOADERS
---------------

Program loaders are classes responsible for loading resources.
Custom loaders can easily be created.

Programs have a default set of loaders if not specified.

.. code:: python

    PROGRAM_LOADERS = (
        'demosys.loaders.program.single.Loader',
        'demosys.loaders.program.separate.Loader',
    )

TEXTURE_DIRS/TEXTURE_FINDERS
----------------------------

Same principle as ```PROGRAM`_DIRS`` and ``PROGRAM_FINDERS``.
The ``EffectDirectoriesFinder`` will look for a ``textures`` directory in effects.

.. code:: python

    # Finder classes
    TEXTURE_FINDERS = (
        'demosys.core.texturefiles.finders.FileSystemFinder',
        'demosys.core.texturefiles.finders.EffectDirectoriesFinder'
    )

    # Absolute path to a project-global texture directory
    TEXTURE_DIRS = (
        os.path.join(PROJECT_DIR, 'resources/textures'),
    )

TEXTURE_LOADERS
----------------

Texture loaders are classes responsible for loading textures.
These can be easily customized.

The default texture loaders:

.. code:: python

    TEXTURE_LOADERS = (
        'demosys.loaders.texture.t2d.Loader',
        'demosys.loaders.texture.array.Loader',
    )


SCENE_DIRS/SCENE_FINDERS
------------------------

Same principle as ``PROGRAM_DIRS`` and ``PROGRAM_FINDERS``.
This is where scene files such as wavefront and gltf files are loaded from.
The ``EffectDirectoriesFinder`` will look for a ``scenes`` directory

.. code:: python

    # Finder classes
    SCENE_FINDERS = (
        'demosys.core.scenefiles.finders.FileSystemFinder',
        'demosys.core.scenefiles.finders.EffectDirectoriesFinder'
    )

    # Absolute path to a project-global scene directory
    SCENE_DIRS = (
        os.path.join(PROJECT_DIR, 'resources/scenes'),
    )

SCENE_LOADERS
-------------

Scene loaders are classes responsible for loading scenes or geometry
from different formats.

The default scene loaders are:

.. code:: python

    SCENE_LOADERS = (
        "demosys.loaders.scene.gltf.GLTF2",
        "demosys.loaders.scene.wavefront.ObjLoader",
    )

DATA_DIRS/DATA_FINDERS
----------------------

Same principle as ``PROGRAM_DIRS`` and ``PROGRAM_FINDERS``.
This is where the system looks for data files. These are
generic loaders for binary, text and json data (or anything you want).

.. code:: python

    # Finder classes
    DATA_FINDERS = (
        'demosys.core.scenefiles.finders.FileSystemFinder',
        'demosys.core.scenefiles.finders.EffectDirectoriesFinder'
    )

    # Absolute path to a project-global scene directory
    DATA_DIRS = (
        os.path.join(PROJECT_DIR, 'resources/scenes'),
    )

DATA_LOADERS
------------

Data loaders are classes responsible for loading miscellaneous
data files. These are fairly easy to implement
if you need to support something custom.

The default data loaders are:

.. code:: python

    DATA_LOADERS = (
        'demosys.loaders.data.binary.Loader',
        'demosys.loaders.data.text.Loader',
        'demosys.loaders.data.json.Loader',
    )

.. _pyrocket: https://github.com/Contraz/pyrocket
