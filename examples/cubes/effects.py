import moderngl
from demosys import geometry
from demosys.effects import Effect


class Cubes(Effect):
    """
    Slightly overkill example showing we can instantiate
    other effects inside an effect

    We draw three cubes with different properties
    """
    runnable = True

    def __init__(self):
        self.cube = geometry.cube(4.0, 4.0, 4.0)

        # Instantiate the cube effects
        # This would normally be done in project
        self.plain = PlainCube(self.cube)
        self.light = LightCube(self.cube)
        self.textured = TexturedCube(self.cube)

    def draw(self, time, frametime, target):
        self.ctx.enable(moderngl.DEPTH_TEST)

        self.plain.draw(time, frametime, target)
        self.light.draw(time, frametime, target)
        self.textured.draw(time, frametime, target)


class PlainCube(Effect):
    """Tha plain colored cube"""
    # Not runnable because it relies on the Cube effect
    runnable = False

    def __init__(self, cube):
        self.cube = cube
        self.program = self.get_program("plain")

    def draw(self, time, frametime, target):
        m_mv = self.create_transformation(rotation=(time * 1.2, time * 2.1, time * 0.25),
                                          translation=(-7.0, 0.0, -12.0))

        self.program.uniform("m_proj", self.sys_camera.projection.tobytes())
        self.program.uniform("m_mv", m_mv.astype('f4').tobytes())
        self.cube.draw(self.program)


class LightCube(Effect):
    """Simple light cube"""
    # Not runnable because it relies on the Cube effect
    runnable = False

    def __init__(self, cube):
        self.cube = cube
        self.program = self.get_program("light")

    def draw(self, time, frametime, target):
        m_mv = self.create_transformation(rotation=(time * 1.2, time * 2.1, time * 0.25),
                                          translation=(0.0, 0.0, -12.0))
        m_normal = self.create_normal_matrix(m_mv)

        self.program.uniform("m_proj", self.sys_camera.projection.tobytes())
        self.program.uniform("m_mv", m_mv.astype('f4').tobytes())
        self.program.uniform("m_normal", m_normal.astype('f4').tobytes())
        self.cube.draw(self.program)


class TexturedCube(Effect):
    """Textued cube with light"""
    # Not runnable because it relies on the Cube effect
    runnable = False

    def __init__(self, cube):
        self.cube = cube
        self.program = self.get_program("textured")
        self.texture = self.get_texture("crate")

    def draw(self, time, frametime, target):
        m_mv = self.create_transformation(rotation=(time * 1.2, time * 2.1, time * 0.25),
                                          translation=(7.0, 0.0, -12.0))
        m_normal = self.create_normal_matrix(m_mv)

        self.program.uniform("m_proj", self.sys_camera.projection.tobytes())
        self.program.uniform("m_mv", m_mv.astype('f4').tobytes())
        self.program.uniform("m_normal", m_normal.astype('f4').tobytes())
        self.texture.use(location=0)
        self.program.uniform("wood", 0)
        self.cube.draw(self.program)
