from demosys.effects import effect
from demosys import geometry
from OpenGL import GL
from pyrr import matrix44


class TexturedSphere(effect.Effect):
    """Generated default effect"""
    def __init__(self):
        self.shader = self.get_shader("default.glsl", local=True)
        self.sphere = geometry.sphere(4.0, sectors=32, rings=16)
        self.texture = self.get_texture("wood.jpg", local=True)

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
        self.shader.uniform("m_proj", self.sys_camera.projection.tobytes())
        self.shader.uniform("m_mv", m_mv.astype('f4').tobytes())
        self.shader.uniform("m_normal", m_normal.astype('f4').tobytes())
        self.texture.use(location=0)
        self.shader.uniform("texture0", 0)
        self.sphere.draw(self.shader)
