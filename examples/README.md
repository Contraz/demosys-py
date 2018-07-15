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
