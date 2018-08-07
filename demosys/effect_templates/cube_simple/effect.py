import moderngl
from demosys import geometry
from demosys.effects import effect

# from pyrr import matrix44


class SimpleCubeEffect(effect.Effect):
    """Generated default effect"""
    def __init__(self):
        self.program = self.get_program("cube_plain.glsl", local=True)
        self.cube = geometry.cube(4.0, 4.0, 4.0)

    def draw(self, time, frametime, target):
        self.ctx.enable(moderngl.DEPTH_TEST)

        # Rotate and translate
        m_mv = self.create_transformation(rotation=(time * 1.2, time * 2.1, time * 0.25),
                                          translation=(0.0, 0.0, -8.0))

        # Apply the rotation and translation from the system camera
        # m_mv = matrix44.multiply(m_mv, self.sys_camera.view_matrix)

        # Create normal matrix from model-view
        m_normal = self.create_normal_matrix(m_mv)

        # Draw the cube
        self.program.uniform("m_proj", self.sys_camera.projection.tobytes())
        self.program.uniform("m_mv", m_mv.astype('f4').tobytes())
        self.program.uniform("m_normal", m_normal.astype('f4').tobytes())
        self.program.uniform("time", time)
        self.cube.draw(self.program)
