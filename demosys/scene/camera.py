from pyrr import matrix44, vector3, vector, Vector3


class Camera:
    """Simple camera class containing projection"""
    def __init__(self, fov=60, aspect=1.0, near=1, far=100):
        """
        Initialize camera using a specific projeciton        
        :param fov: Field of view
        :param aspect: Aspect ratio
        :param near: Near plane
        :param far: Far plane
        """
        self.fov = fov
        self.aspect = aspect
        self.near = near
        self.far = far
        self.position = None
        self.set_position(0.0, 0.0, 0.0)
        self._up = Vector3([0.0, 1.0, 0.0])
        self._update_projection()

    def set_position(self, x, y, z):
        self.position = Vector3([x, y, z])

    def update_projection(self, fov=None, aspect=None, near=None, far=None):
        """
        Update projection parameters
        :param fov: Field of view
        :param aspect: Aspect ratio
        :param near: Near plane
        :param far: Far plane
        """
        self.fov = fov or self.fov
        self.near = near or self.near
        self.far = far or self.far
        self.aspect = aspect or self.aspect
        self._update_projection()

    def look_at(self, vec=None, pos=None):
        """
        Look at a specific point
        :param vec: Vector3 position
        :param pos: python list [x, y, x]
        :return: Camera matrix
        """
        if pos:
            vec = Vector3(pos)
        if vec is None:
            raise ValueError("vector or pos must be set")
        return self._gl_look_at(self.position, vec, self._up)

    def _gl_look_at(self, pos, target, up):
        """
        The standard lookAt method
        :param pos: current position
        :param target: target position to look at
        :param up: direction up
        """
        z = vector.normalise(pos - target)
        x = vector.normalise(vector3.cross(vector.normalise(up), z))
        y = vector3.cross(z, x)

        translate = matrix44.create_identity()
        translate[3][0] = -pos.x
        translate[3][1] = -pos.y
        translate[3][2] = -pos.z

        rotate = matrix44.create_identity()
        rotate[0][0] = x[0]  # -- X
        rotate[1][0] = x[1]
        rotate[2][0] = x[2]
        rotate[0][1] = y[0]  # -- Y
        rotate[1][1] = y[1]
        rotate[2][1] = y[2]
        rotate[0][2] = z[0]  # -- Z
        rotate[1][2] = z[1]
        rotate[2][2] = z[2]

        # return matrix44.multiply(rotate, translate)
        return matrix44.multiply(translate, rotate)

    def _update_projection(self):
        self.projection = matrix44.create_perspective_projection_matrix(
            self.fov, self.aspect, self.near, self.far)
