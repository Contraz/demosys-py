import math
import random

import numpy
from pyrr import matrix44, vector3

import moderngl as mgl
from demosys.effects import effect
from demosys.opengl import VAO


class FeedbackEffect(effect.Effect):

    def __init__(self):
        self.feedback = self.get_program("transform")
        self.program = self.get_program("billboards")
        self.texture = self.get_texture("particle")

        # VAOs representing the two different buffer bindings
        self.particles1 = None
        self.particles2 = None
        self.particles = None

        # VBOs for each position buffer
        self.pos1 = None
        self.pos2 = None
        self.pos = None
        self.init_particles()

    def draw(self, time, frametime, target):
        self.ctx.disable(mgl.DEPTH_TEST)
        self.ctx.enable(mgl.BLEND)
        self.ctx.blend_func = mgl.SRC_ALPHA, mgl.ONE_MINUS_SRC_ALPHA

        m_proj = self.create_projection(90.0, 1.0, 1000.0)

        # Rotate and translate
        m_mv = self.create_transformation(rotation=(time * 0.0, time * 0, time * 0),
                                          translation=(0.0, 0.0, -40.0))

        # Apply the rotation and translation from the system camera
        m_mv = matrix44.multiply(m_mv, self.sys_camera.view_matrix)

        gravity_pos = vector3.create(math.sin(time) * 5,
                                     math.cos(time) * 5,
                                     math.sin(time / 3) * 5)
        gravity_force = math.cos(time / 2) * 3.0 + 3.0
        # gravity_force = 2.0

        # Transform positions
        self.feedback["gravity_pos"].write(gravity_pos.astype('f4').tobytes())
        self.feedback["gravity_force"].value = gravity_force
        self.feedback["timedelta"].value = frametime
        self.particles.transform(self.feedback, self.pos)

        # Draw particles
        self.program["m_proj"].write(m_proj.astype('f4').tobytes())
        self.program["m_mv"].write(m_mv.astype('f4').tobytes())
        self.texture.use(location=0)
        self.program["texture0"].value = 0
        self.particles.draw(self.program)

        # Swap buffers
        self.pos = self.pos1 if self.pos == self.pos2 else self.pos2
        self.particles = self.particles1 if self.particles == self.particles2 else self.particles2

    def init_particles(self):
        count = 50000
        area = 100.0
        speed = 5.0

        def gen():
            for _ in range(count):
                # Position
                yield random.uniform(-area, area)
                yield random.uniform(-area, area)
                yield random.uniform(-area, area)
                # Velocity
                yield random.uniform(-speed, speed)
                yield random.uniform(-speed, speed)
                yield random.uniform(-speed, speed)

        data1 = numpy.fromiter(gen(), count=count * 6, dtype=numpy.float32)
        data2 = numpy.fromiter(gen(), count=count * 6, dtype=numpy.float32)

        self.pos1 = self.ctx.buffer(data1.tobytes())
        self.particles1 = VAO("particles1", mode=mgl.POINTS)
        self.particles1.buffer(self.pos1, '3f 3f', ['in_position', 'in_velocity'])

        self.pos2 = self.ctx.buffer(data2.tobytes())
        self.particles2 = VAO("particles2", mode=mgl.POINTS)
        self.particles2.buffer(self.pos2, '3f 3f', ['in_position', 'in_velocity'])

        # Set initial start buffers
        self.particles = self.particles1
        self.pos = self.pos2
