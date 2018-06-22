from pyrr import Matrix44


class Projection:
    """
    Represent a projection matrix and its various properties
    including tools.
    """
    def __init__(self, aspect_ratio=9 / 16, fov=75, near=1, far=100):
        self.aspect_ratio = aspect_ratio
        self.fov = fov
        self.near = near
        self.far = far
        self.matrix = None
        self.update()

    def update(self, aspect_ratio=None, fov=None, near=None, far=None):
        """
        Update the internal projection matrix based on current values
        or values passed in if specified.

        :param aspect_ratio: New aspect ratio
        :param fov: New field of view
        :param near: New near value
        :param far: New far value
        """
        self.aspect_ratio = aspect_ratio or self.aspect_ratio
        self.fov = fov or self.fov
        self.near = near or self.near
        self.far = far or self.far

        self.matrix = Matrix44.perspective_projection(self.fov, self.aspect_ratio, self.near, self.far)

    def tobytes(self):
        return self.matrix.astype('f4').tobytes()

    @property
    def projection_constants(self):
        """
        Returns the (x, y) projection constants for the current projection.
        :return: x, y tuple projection constants
        """
        return self.far / (self.far - self.near), (self.far * self.near) / (self.near - self.far)
