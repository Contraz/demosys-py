import moderngl
from demosys import geometry
from demosys.effects import effect
# from pyrr import matrix44


class SimpleCubeEffect(effect.Effect):
    runnable = True

    def __init__(self):
        # Obtain the shader program using its label
        self.program = self.get_program('cube_plain')
        # Create a 4x4x4 cube with center in (0, 0, 0)
        self.cube = geometry.cube(4.0, 4.0, 4.0)

    def draw(self, time, frametime, target):
        # Enable depth testing and face fulling
        self.ctx.enable(moderngl.DEPTH_TEST | moderngl.CULL_FACE)

        # Rotate and translate (modelview matrix)
        m_mv = self.create_transformation(rotation=(time * 1.2, time * 2.1, time * 0.25),
                                          translation=(0.0, 0.0, -8.0))

        # Uncomment to Apply the rotation and translation from the system camera
        # m_mv = matrix44.multiply(m_mv, self.sys_camera.view_matrix)

        # Create normal matrix from model-view
        m_normal = self.create_normal_matrix(m_mv)

        # Write to the shader programs uniforms
        self.program["m_proj"].write(self.sys_camera.projection.tobytes())
        self.program["m_mv"].write(m_mv.astype('f4').tobytes())
        self.program["m_normal"].write(m_normal.astype('f4').tobytes())
        self.program["time"].value = time

        # Render the cube
        self.cube.render(self.program)
