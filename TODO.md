
## TODO

Find more efficient OpenGL bindings. ModernGL (https://pypi.python.org/pypi/ModernGL) 
don't have a binary distribution for darwin.

- Framebuffer Blitting
- Properly verify all settings
- Make EffectControllers
  - TrackSystemEffectController
  - SimpleTimeLineEffectManager
- Shaders
  - Improve error prints (use actual source from GL so we can see expanded typedefs)
  - Core loader support for common formats
  - Custom loader support / less hacky loading
Textures:
  - 3D
  - Texture Array
  - Texture Cube
- Custom texture loaders
- FBOs
  - Support layers
Generic Data:
  - Custom resource loaders ("misc stuff")
- Mesh / Scene?
  - Custom mesh / scene loading
- Debug Windows?
  - FBOs
  - Textures
- Settings entry for key bindings
- Look into using freetype or some kind of fonts
