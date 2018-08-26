
2.0.1
-----

* Resolved a problem with the distributuon causing some packages to not be included. This was related to implicit namespace packages
* Project template now contains a basic project

2.0.0
-----

* The FBO class is gone. Use ``moderngl.Framebuffer`` or ``moderngl.RenderBuffer`` directly instead.
* Effect no longer have ``window_width`` and ``window_height`` properties. Use ``Effect.window.<property>`` instead.
* The effect ``bind_target`` decorator no longer exists
* All loaders moved to ``demosys.loaders``
* All texture wrapper classes are gone. We only work on moderngl types directly
* Texture and FBO draw functions can instead be found in ``demosys.opengl.texture``
* Created a texture loading system. ``settings.TEXTURE_LOADERS`` can changed to custom types
