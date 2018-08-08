from pyrr import matrix44

import moderngl
from demosys import geometry
from demosys.effects import effect


class TexturedSphere(effect.Effect):
    """Generated default effect"""
    def __init__(self):
        self.program = self.get_program("default.glsl", local=True)
        self.sphere = geometry.sphere(4.0, sectors=32, rings=16)
        self.texture = self.get_texture("wood.jpg", local=True)

    def draw(self, time, frametime, target):
        self.ctx.enable(moderngl.DEPTH_TEST)
        self.ctx.enable(moderngl.CULL_FACE)
        self.ctx.front_face = 'ccw'

        # Rotate and translate
        m_mv = self.create_transformation(rotation=(time * 1.2, time * 2.1, time * 0.25),
                                          translation=(0.0, 0.0, -8.0))

        # Apply the rotation and translation from the system camera
        m_mv = matrix44.multiply(m_mv, self.sys_camera.view_matrix)

        # Create normal matrix from model-view
        m_normal = self.create_normal_matrix(m_mv)

        # Draw the cube
        self.program.uniform("m_proj", self.sys_camera.projection.tobytes())
        self.program.uniform("m_mv", m_mv.astype('f4').tobytes())
        self.program.uniform("m_normal", m_normal.astype('f4').tobytes())
        self.texture.use(location=0)
        self.program.uniform("texture0", 0)
        self.sphere.draw(self.program)
