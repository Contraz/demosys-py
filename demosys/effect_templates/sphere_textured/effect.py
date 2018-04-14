from demosys.effects import effect
from demosys.opengl import geometry
from OpenGL import GL
from pyrr import matrix44


class TexturedSphere(effect.Effect):
    """Generated default effect"""
    def __init__(self):
        self.shader = self.get_shader("default.glsl")
        self.sphere = geometry.sphere(4.0, sectors=32, rings=16)
        self.texture = self.get_texture("wood.jpg")

    @effect.bind_target
    def draw(self, time, frametime, target):
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_CULL_FACE)
        GL.glFrontFace(GL.GL_CCW)

        # Rotate and translate
        m_mv = self.create_transformation(rotation=(time * 1.2, time * 2.1, time * 0.25),
                                          translation=(0.0, 0.0, -8.0))

        # Apply the rotation and translation from the system camera
        m_mv = matrix44.multiply(m_mv, self.sys_camera.view_matrix)

        # Create normal matrix from model-view
        m_normal = self.create_normal_matrix(m_mv)

        # Draw the cube
        with self.sphere.bind(self.shader) as s:
            s.uniform_mat4("m_proj", self.sys_camera.projection.matrix)
            s.uniform_mat4("m_mv", m_mv)
            s.uniform_mat3("m_normal", m_normal)
            s.uniform_sampler_2d(0, "texture0", self.texture)
        self.sphere.draw()
