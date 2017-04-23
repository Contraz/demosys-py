
Temporary Notes
===============

This needs to be restructured into actual docs.

- The ``cube`` objects is a ``VAO`` that you bind supplying the shader and the system
  will figure out the attribute mapping.
- You currently define vertex,
  fragment and geometry shader in one glsl file separated by
  preprocessors.


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
- The ``time`` value passed to the effects ``draw`` method is the current
  duration in the playing music. If no music is loaded, a dummy timer is used.

.. _testdemo: https://github.com/Contraz/demosys-py-test
