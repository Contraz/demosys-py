from math import sin, cos, radians
import glfw
from pyrr import matrix44, vector3, vector, Vector3
from demosys.opengl import Projection

# Direction Definitions
RIGHT = 1
LEFT = 2
FORWARD = 3
BACKWARD = 4
UP = 5
DOWN = 6

# Movement Definitions
STILL = 0
POSITIVE = 1
NEGATIVE = 2


class Camera:
    """Simple camera class containing projection"""
    def __init__(self, fov=60, aspect=1.0, near=1, far=100):
        """
        Initialize camera using a specific projection

        :param fov: Field of view
        :param aspect: Aspect ratio
        :param near: Near plane
        :param far: Far plane
        """
        self.position = Vector3([0.0, 0.0, 0.0])
        # Default camera placement
        self.up = Vector3([0.0, 1.0, 0.0])
        self.right = Vector3([1.0, 0.0, 0.0])
        self.dir = Vector3([0.0, 0.0, -1.0])
        # Yaw and Pitch
        self.yaw = -90.0
        self.pitch = 0.0

        # World up vector
        self._up = Vector3([0.0, 1.0, 0.0])

        # Projection
        self.projection = Projection(aspect, fov, near, far)

    def set_position(self, x, y, z):
        """
        Set the 3D position of the camera

        :param x: float
        :param y: float
        :param z: float
        """
        self.position = Vector3([x, y, z])

    @property
    def view_matrix(self):
        """
        :return: The current view matrix for the camera
        """
        self._update_yaw_and_pitch()
        return self._gl_look_at(self.position, self.position + self.dir, self._up)

    def _update_yaw_and_pitch(self):
        """
        Updates the camera vectors based on the current yaw and pitch
        """
        front = Vector3([0.0, 0.0, 0.0])
        front.x = cos(radians(self.yaw)) * cos(radians(self.pitch))
        front.y = sin(radians(self.pitch))
        front.z = sin(radians(self.yaw)) * cos(radians(self.pitch))

        self.dir = vector.normalise(front)
        self.right = vector.normalise(vector3.cross(self.dir, self._up))
        self.up = vector.normalise(vector3.cross(self.right, self.dir))

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

        return matrix44.multiply(translate, rotate)


class SystemCamera(Camera):
    """System camera controlled by mouse and keyboard"""
    def __init__(self, fov=60, aspect=1.0, near=1, far=100):
        # Position movement states
        self._xdir = STILL
        self._zdir = STILL
        self._ydir = STILL
        self._last_time = 0
        # Velocity in axis units per second
        self.velocity = 10.0
        self.mouse_sensitivity = 0.5
        self.last_x = None
        self.last_y = None

        super().__init__(fov=fov, aspect=aspect, near=near, far=far)

    def move_state(self, direction, activate):
        """
        Set the camera position move state

        :param direction: What direction to update
        :param activate: Start or stop moving in the direction
        """
        if direction == RIGHT:
            self._xdir = POSITIVE if activate else STILL
        elif direction == LEFT:
            self._xdir = NEGATIVE if activate else STILL
        elif direction == FORWARD:
            self._zdir = NEGATIVE if activate else STILL
        elif direction == BACKWARD:
            self._zdir = POSITIVE if activate else STILL
        elif direction == UP:
            self._ydir = POSITIVE if activate else STILL
        elif direction == DOWN:
            self._ydir = NEGATIVE if activate else STILL

    def rot_state(self, x, y):
        """
        Set the rotation state of the camera

        :param x: viewport x pos
        :param y: viewport y pos
        """
        if self.last_x is None:
            self.last_x = x
        if self.last_y is None:
            self.last_y = y

        x_offset = self.last_x - x
        y_offset = self.last_y - y

        self.last_x = x
        self.last_y = y

        x_offset *= self.mouse_sensitivity
        y_offset *= self.mouse_sensitivity

        self.yaw -= x_offset
        self.pitch += y_offset

        if self.pitch > 85.0:
            self.pitch = 85.0
        if self.pitch < -85.0:
            self.pitch = -85.0

        self._update_yaw_and_pitch()

    @property
    def view_matrix(self):
        """
        :return: The current view matrix for the camera
        """
        # Use separate time in camera so we can move it when the demo is paused
        time = glfw.get_time()
        # If the camera has been inactive for a while, a large time delta
        # can suddenly move the camera far away from the scene
        t = max(time - self._last_time, 0)
        self._last_time = time

        # X Movement
        if self._xdir == POSITIVE:
            self.position += self.right * self.velocity * t
        elif self._xdir == NEGATIVE:
            self.position -= self.right * self.velocity * t

        # Z Movement
        if self._zdir == NEGATIVE:
            self.position += self.dir * self.velocity * t
        elif self._zdir == POSITIVE:
            self.position -= self.dir * self.velocity * t

        # Y Movement
        if self._ydir == POSITIVE:
            self.position += self.up * self.velocity * t
        elif self._ydir == NEGATIVE:
            self.position -= self.up * self.velocity * t

        return self._gl_look_at(self.position, self.position + self.dir, self._up)
