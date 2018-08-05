
2.0.0
-----

* The FBO class is gone. Use ``moderngl.Framebuffer`` or ``moderngl.RenderBuffer`` directly instead.
* Effect no longer have ``window_width`` and ``window_height`` properties. Use ``Effect.window.<property>`` instead.
* The effect ``bind_target`` decorator no longer exists
* All loaders moved to ``demosys.loaders``

Expand on:
* Texture and FBO draw functions
