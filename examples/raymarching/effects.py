import math

from pyrr import Vector3

import moderngl
from demosys import geometry
from demosys.effects import effect


class SimpleRaymarchEffect(effect.Effect):
    """Generated raymarching effect"""
    def __init__(self):
        self.program = self.get_program("raymarching_simple")

        # create plane to fit whole screen
        self.plane = geometry.plane_xz(size=self.window.size, resolution=(10, 10))

    def draw(self, time, frametime, target):
        self.ctx.enable(moderngl.DEPTH_TEST)

        # Rotate plane 90 degrees, and move plane back so it will fit correctly on to screen
        backoff = math.tan(math.radians(self.sys_camera.projection.fov / 2)) * (self.window.width / 2)
        m_mv = self.create_transformation(rotation=(math.radians(90), 0.0, 0.0), translation=(0.0, 0.0, -backoff))

        # Uniforms
        fov = 0.60
        alpha = 1.0
        modifier = -0.6
        cPosition = Vector3([(math.sin(time / 6.0) * 16.0),
                             (math.sin(time / 12.0) * 16.0),
                             (math.cos(time / 3.0) * 16.0)])
        cLookAt = Vector3([0.0, 0.0, 0.0])
        lPosition = Vector3([0.0, 17.0, 0.0])
        lItensity = 2.6
        color = Vector3([0.66, 0.96, 0.26])

        # Draw the plane

        # For vertex program
        self.program["m_proj"].write(self.sys_camera.projection.tobytes())
        self.program["m_mv"].write(m_mv.astype('f4').tobytes())

        # For fragment program
        self.program["fov"].value = fov
        self.program["alpha"].value = alpha
        self.program["modifier"].value = modifier

        self.program["cPosition"].write(cPosition.astype('f4').tobytes())
        self.program["cLookAt"].write(cLookAt.astype('f4').tobytes())
        self.program["lPosition"].write(lPosition.astype('f4').tobytes())
        self.program["lIntensity"].value = lItensity
        self.program["color"].write(color.astype('f4').tobytes())

        self.program["resolution"].value = (self.window.width, self.window.height)

        self.plane.render(self.program)
