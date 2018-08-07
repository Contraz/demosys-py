import moderngl
from demosys import geometry
from demosys.effects import effect


class SimpleCubeEffect(effect.Effect):
    """Generated default effect"""
    def __init__(self):
        self.plain_prog = self.get_program("plain")
        self.light_prog = self.get_program("light")
        self.texture_prog = self.get_program("textured")
        self.texture = self.get_texture("crate")
        self.cube = geometry.cube(4.0, 4.0, 4.0)

    def draw(self, time, frametime, target):
        self.ctx.enable(moderngl.DEPTH_TEST)

        # Plain Cube
        m_mv = self.create_transformation(rotation=(time * 1.2, time * 2.1, time * 0.25),
                                          translation=(-7.0, 0.0, -12.0))

        self.plain_prog.uniform("m_proj", self.sys_camera.projection.tobytes())
        self.plain_prog.uniform("m_mv", m_mv.astype('f4').tobytes())
        self.cube.draw(self.plain_prog)

        # Light Cube
        m_mv = self.create_transformation(rotation=(time * 1.2, time * 2.1, time * 0.25),
                                          translation=(0.0, 0.0, -12.0))
        m_normal = self.create_normal_matrix(m_mv)

        self.light_prog.uniform("m_proj", self.sys_camera.projection.tobytes())
        self.light_prog.uniform("m_mv", m_mv.astype('f4').tobytes())
        self.light_prog.uniform("m_normal", m_normal.astype('f4').tobytes())
        self.cube.draw(self.light_prog)

        # Textured cube
        m_mv = self.create_transformation(rotation=(time * 1.2, time * 2.1, time * 0.25),
                                          translation=(7.0, 0.0, -12.0))
        m_normal = self.create_normal_matrix(m_mv)

        self.texture_prog.uniform("m_proj", self.sys_camera.projection.tobytes())
        self.texture_prog.uniform("m_mv", m_mv.astype('f4').tobytes())
        self.texture_prog.uniform("m_normal", m_normal.astype('f4').tobytes())
        self.texture.use(location=0)
        self.texture_prog.uniform("wood", 0)
        self.cube.draw(self.texture_prog)
