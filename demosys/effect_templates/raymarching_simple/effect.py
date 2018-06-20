from demosys.effects import effect
from demosys.opengl import geometry
from OpenGL import GL
import math

class SimpleRaymarchEffect(effect.Effect):
    """Generated raymarching effect"""
    def __init__(self):
        self.shader = self.get_shader("raymarching_simple.glsl")
        # create plane to fit whole screen
        self.plane = geometry.plane.plane_xz(size=(self.window_width, self.window_height), resolution=(10, 10))

    @effect.bind_target
    def draw(self, time, frametime, target):
        GL.glEnable(GL.GL_DEPTH_TEST)

        # Rotate plane 90 degrees, and move plane back so it will fit correctly on to screen
        backoff = math.tan(math.radians(self.sys_camera.projection.fov / 2)) * (self.window_width / 2)
        m_mv = self.create_transformation(rotation=(math.radians(90), 0.0, 0.0), translation=(0.0, 0.0, -backoff))

        # Create normal matrix from model-view
        m_normal = self.create_normal_matrix(m_mv)

        # Draw the quad
        with self.plane.bind(self.shader) as shader:
            shader.uniform_mat4("m_proj", self.sys_camera.projection.matrix)
            shader.uniform_mat4("m_mv", m_mv)
            shader.uniform_mat3("m_normal", m_normal)
            shader.uniform_1f("time", time)
        self.plane.draw()
