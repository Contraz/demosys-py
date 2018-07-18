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
