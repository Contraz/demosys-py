
Temporary Notes
===============

This needs to be restructured into actual docs.

- Shaders and textures can be easily loaded by using the ``get_texture`` and
  ``get_shader`` method inherited from ``Effect``.
- The ``cube`` objects is a ``VAO`` that you bind supplying the shader and the system
  will figure out the attribute mapping.
- Please look in the ``demosys.opengl.geometry`` module for the valid attribute names and
  look at shaders in the testdemo_.
- You currently define vertex,
  fragment and geometry shader in one glsl file separated by
  preprocessors.
- Effects not defined in the ``settings.py`` module will not run.

That should give you an idea..

Anything we draw to the screen must be implemented as an ``Effect``. If
that effect is one or multiple things is entirely up to you. An effect
is an individual package/directory containing an ``effect.py`` module.
This package can also contain a ``shaders`` and ``textures`` directory
that demosys will automatically find and load resources from. See the
testdemo_.

Explore the testdemo_ project, and you'll get the point.

Some babble about the current state of the project:

- All geometry must be defined using VAOs. There's a very convenient VAO
  class for this already making it quick and easy to create them. Look at
  the ``demosys.opengl.geometry`` module for examples.
- We support vertex,
  fragment and geometry shaders for now. A program must currently be
  written in one single ``.glsl`` file separating the shaders with
  preprocessors. See existing shaders in testdemo_.
- The Shader class will inspect the linked shader and cache all attributes
  and uniforms in local dictionaries. This means all ``uniform*``-setters use
  the name of the uniform instead of the location. Location is resolved
  internally in the object/class.
- The VAOs ``bind(..)`` requires you to pass in a shader. This is because
  the VAO will automatically adapt to the attributes in your shader.
  During the VAO creation you need to make the name mapping to the attribute
  name. If you have a VAO with positions, normals, uvs and tangents and pass
  in a shader that only use position (or any other combination of attributes
  in the VAO); the VAO class will on-the-fly generate a version internally
  with only positions.
- We only support 2D textures at the moment loaded with PIL/Pillow, but
  this is trivial to extend.
- Resource loading is supported in the ``Effect`` class itself. In ``__init__()``
  you can fetch resources using for example ``self.get_shader`` or\ ``self.get_texture``.
  This will return a lazy object that will be populated after the loading
  stage is done.
- Resources shared between effects can be put outside effect packages
  inside your project directory. For example in ``testdemo/resources/shaders``
  and ``testdemo/resources/textures``. Make sure you add those paths in the
  settings file.
- We don't have any scene/mesh loaders. You can hack something in yourself
  for now or just stick to or extend the ``geometry`` module. - We try to
  do as much validation as possible and give useful feedback when something
  goes wrong.
- The ``time`` value passed to the effects ``draw`` method is the current
  duration in the playing music. If no music is loaded, a dummy timer is used.

.. _testdemo: https://github.com/Contraz/demosys-py-test
