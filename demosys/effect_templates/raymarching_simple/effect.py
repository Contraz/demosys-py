from demosys.effects import effect
from demosys.opengl import geometry
from OpenGL import GL
# from pyrr import matrix44


class SimpleRaymarchEffect(effect.Effect):
    """Generated raymarching effect"""
    def __init__(self):
        self.shader = self.get_shader("raymarching_simple.glsl")
        self.quad = geometry.quad.quad_2d(1, 1)

    @effect.bind_target
    def draw(self, time, frametime, target):
        GL.glEnable(GL.GL_DEPTH_TEST)

        # Rotate and translate
        m_mv = self.create_transformation(rotation=(0.0, 0.0, 0.0),
                                          translation=(0.0, 0.0, -1.0))

        # Apply the rotation and translation from the system camera
        # m_mv = matrix44.multiply(m_mv, self.sys_camera.view_matrix)

        # Create normal matrix from model-view
        m_normal = self.create_normal_matrix(m_mv)

        # Draw the cube
        with self.quad.bind(self.shader) as shader:
            shader.uniform_mat4("m_proj", self.sys_camera.projection.matrix)
            shader.uniform_mat4("m_mv", m_mv)
            shader.uniform_mat3("m_normal", m_normal)
            shader.uniform_1f("time", time)
        self.quad.draw()
