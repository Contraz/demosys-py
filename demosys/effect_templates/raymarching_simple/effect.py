import moderngl as mgl

from demosys.effects import effect
from demosys import geometry
from pyrr import Vector3
import math


class SimpleRaymarchEffect(effect.Effect):
    """Generated raymarching effect"""
    def __init__(self):
        self.shader = self.get_shader("raymarching_simple.glsl", local=True)

        # create plane to fit whole screen
        self.plane = geometry.plane.plane_xz(size=(self.window_width, self.window_height), resolution=(10, 10))

    @effect.bind_target
    def draw(self, time, frametime, target):
        self.ctx.enable(mgl.DEPTH_TEST)

        # Rotate plane 90 degrees, and move plane back so it will fit correctly on to screen
        backoff = math.tan(math.radians(self.sys_camera.projection.fov / 2)) * (self.window_width / 2)
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

        # For vertex shader
        self.shader.uniform("m_proj", self.sys_camera.projection.tobytes())
        self.shader.uniform("m_mv", m_mv.astype('f4').tobytes())

        # For fragment shader
        self.shader.uniform("fov", fov)
        self.shader.uniform("alpha", alpha)
        self.shader.uniform("modifier", modifier)

        self.shader.uniform("cPosition", cPosition.astype('f4').tobytes())
        self.shader.uniform("cLookAt", cLookAt.astype('f4').tobytes())
        self.shader.uniform("lPosition", lPosition.astype('f4').tobytes())
        self.shader.uniform("lIntensity", lItensity)
        self.shader.uniform("color", color.astype('f4').tobytes())

        self.shader.uniform("resolution", (self.window_width, self.window_height))

        self.plane.draw(self.shader)
