Examples
========

All examples must run from the root of the repository where ``manage.py`` is located.

Cubes
-----

Simple example showing three cubes

* Single Color
* Lighting
* Textured

```bash
python manage.py runeffect examples.cubes
```

![screenshot](https://raw.githubusercontent.com/Contraz/demosys-py/master/examples/images/cubes.png)

Texture source : http://free-texture-site.blogspot.com/2010/10/free-game-crate-texture.html

Feedback
--------

Basic example of using transform feedback. Thousands of particles are being
affected by newton's law with a pulsing gravity field in the middle of the scene.
Particles are drawn as points were a geometry shader emits billboarded quads.

```bash
python manage.py runeffect examples.feedback
```

![screenshot](https://github.com/Contraz/demosys-py/blob/master/examples/images/feedback.png)

Geo Cubes
---------

Geometry shader example. We're drawing points were the geometry shader emits
a cube on each point and slightly modifying the position of each cube.
The texture on these cube is an fbo texture of a spinning cube just for fun.

```bash
python manage.py runeffect examples.geocubes
```

![screenshot](https://raw.githubusercontent.com/Contraz/demosys-py/master/examples/images/geocubes.png)

Minecraft
---------

Example loading and drawing a wavefront obj file.

Underground city in the "Lost Empire" area from the Vokselia Minecraft world
http://vokselia.com CC BY 3.0 License http://creativecommons.org/licenses/by/3.0/

```bash
python manage.py runeffect examples.minecraft
```

![screenshot](https://raw.githubusercontent.com/Contraz/demosys-py/master/examples/images/minecraft.png)

Sponza
------

Example loading and drawing GLTF 2.0 scenes. The Atrium Sponza Palace, Dubrovnik, is an elegant and improved model created by Frank Meinl. The original Sponza model was created by Marko Dabrovic in early 2002.
See [README.md](https://github.com/Contraz/demosys-py/tree/master/examples/sponza/scenes/sponza/Sponza) for more info.

```bash
python manage.py runeffect examples.sponza
```

![screenshot](https://raw.githubusercontent.com/Contraz/demosys-py/master/examples/images/sponza.png)

Text Writer
-----------

Example loading a text file displaying it on the screen. The text is drawn using instanced rendering
were each instance is a character in the file. This may not be the most efficient way for drivers
emulating instancing. Text renderer (render to texture) is an alternative.

```bash
python manage.py runeffect examples.textwriter
```

![screenshot](https://raw.githubusercontent.com/Contraz/demosys-py/master/examples/images/textwriter.png)

Text Renderer
-------------

Example loading a text file displaying it on the screen. The text is rendered to a texture at initialization.
We simply display the texture each frame. We are limiting the texture height to 8k in this example.

```bash
python manage.py runeffect examples.textrenderer
```

![screenshot](https://raw.githubusercontent.com/Contraz/demosys-py/master/examples/images/textrenderer.png)

Warp Speed
----------

An example of what can be achieved with a relatively simple shader and a fullscreen quad.
Originally created by Erik "Dran" Norby for the demo "Sonic Room".

```bash
python manage.py runeffect examples.warpspeed
```

![screenshot](https://raw.githubusercontent.com/Contraz/demosys-py/master/examples/images/warpspeed.png)

Ray Marching
------------

Ray marching example by Arttu "helgrima" Tamminen.

```bash
python manage.py runeffect examples.raymaching
```

![screenshot](https://raw.githubusercontent.com/Contraz/demosys-py/master/examples/images/raymarching.png)
