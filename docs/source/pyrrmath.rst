
Matrix and Vector math with pyrr
================================

Pyrr has both a procedural and object oriented api.

See `pyrr <https://pyrr.readthedocs.io/en/latest/>`__ for official docs.

.. Note:: We should probably add some more examples here. Feel free to
   make an issue or pull request on github.

Examples
^^^^^^^^

Identity

.. code:: python

    # procedural
    >> m = matrix44.create_identity()
    >> print(m)
    array([[ 1.,  0.,  0.,  0.],
           [ 0.,  1.,  0.,  0.],
           [ 0.,  0.,  1.,  0.],
           [ 0.,  0.,  0.,  1.]])

    # object
    >> m = Matrix44.identity()
    >> print(m)
    array([[ 1.,  0.,  0.,  0.],
           [ 0.,  1.,  0.,  0.],
           [ 0.,  0.,  1.,  0.],
           [ 0.,  0.,  0.,  1.]])

Matrices produced by ``Matrix44`` are also just numpy arrays as the class extends ``numpy.ndarray``.
We can pretty much use the APIs interchangeably unless we rely on a method in the class.
They can both be passed right into shaders as matrix uniforms.

Rotation

.. code:: python

    # Short version
    mat = Matrix44.from_eulers(Vector3(rotation))

    # Long version
    rot_x = matrix44.create_from_x_rotation(rotation[0])
    rot_y = matrix44.create_from_y_rotation(rotation[1])
    rot_z = matrix44.create_from_z_rotation(rotation[2])
    mat = matrix44.multiply(x, y)
    mat = matrix44.multiply(mat, z)

Covert
^^^^^^

.. code:: python

    # mat4 to mat3
    mat3 = Matrix33.from_matrix44(mat)
    # mat3 to mat4
    mat4 = Matrix44.from_matrix33(mat)


Common Mistakes
^^^^^^^^^^^^^^^

Matrices and vectors are just numpy arrays. When multiplying matrices,
use the ``mult`` method/function.

.. code:: python

    mat = matrix44.mult(mat1, mat2)

Using the ``*`` operator would just make a product of the two arrays.
