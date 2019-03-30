import moderngl
from demosys import geometry
from demosys.effects import effect
from pyrr import matrix44, matrix33


class SunSystemEffect(effect.Effect):
    runnable = True

    def __init__(self):
        self.sky_sphere = geometry.sphere(100.0)
        self.sky_texture = self.get_texture('milkyway')
        self.sky_shader = self.get_program('milkyway')

        self.sun_sphere = geometry.sphere(10.0)
        self.sun_shader = self.get_program('sun')
        self.sun_texture = self.get_texture('sun')

        # Matrices
        self.projection_bytes = self.sys_camera.projection.tobytes()
        self.sun_matrix = matrix44.create_identity()

        # Default shader parameters
        self.sky_shader['m_proj'].write(self.projection_bytes)
        self.sky_shader['texture0'].value = 0
        self.sky_texture.use(location=0)

        # self.sun_shader['m_proj'].write(self.projection_bytes)
        # self.sun_shader['texture0'].value = 1

        self.sun_pos = None
        self.earth = EarthEffect(parent=self)

    def draw(self, time, frametime, target):
        # Enable depth testing and face fulling
        self.ctx.disable(moderngl.DEPTH_TEST | moderngl.CULL_FACE)
        cam_mat = self.sys_camera.view_matrix

        # Skybox
        sky_matrix = matrix44.create_from_matrix33(matrix33.create_from_matrix44(cam_mat))
        self.sky_shader['m_mv'].write(sky_matrix.astype('f4').tobytes())
        self.sky_sphere.render(self.sky_shader)

        self.ctx.enable(moderngl.DEPTH_TEST | moderngl.CULL_FACE)

        # Sun position
        self.sun_pos = cam_mat[3][0:3].astype('f4')

        # Sun
        self.sun_shader['m_mv'].write(self.sys_camera.view_matrix.astype('f4').tobytes())
        self.sun_shader['m_proj'].write(self.projection_bytes)
        self.sun_shader['time'].value = time
        self.sun_shader['texture0'].value = 1
        self.sun_texture.use(location=1)
        self.sun_sphere.render(self.sun_shader)

        # Earth
        self.earth.draw(time, frametime, target)


class EarthEffect(effect.Effect):
    runnable = False

    def __init__(self, parent=None):
        self.parent = parent
        self.program = self.get_program('earth')
        self.texture_day = self.get_texture('earth_day')
        self.texture_night = self.get_texture('earth_night')
        self.texture_clouds = self.get_texture('earth_clouds')
        self.sphere = geometry.sphere(2.0, sectors=128, rings=128)

    def draw(self, time, frametime, target):
        matrix = matrix44.multiply(
            # Rotate earth around its own axis
            matrix44.multiply(
                matrix44.create_from_eulers([0.0, 0.0, -time / 5.0]),
                # Translate out from the sun and rotate around it
                matrix44.multiply(
                    matrix44.create_from_translation([-40, 0, 0]),
                    matrix44.create_from_eulers([0, 0, 0])  # time/100.0])
                ),
            ),
            self.sys_camera.view_matrix
        )

        self.program['m_proj'].write(self.sys_camera.projection.tobytes())
        self.program['m_mv'].write(matrix.astype('f4').tobytes())
        self.program['m_proj'].write(self.sys_camera.projection.tobytes())
        self.program['sun_pos'].write(self.parent.sun_pos.tobytes())
        self.program['texture_day'].value = 1
        self.program['texture_night'].value = 2
        self.program['texture_clouds'].value = 3
        self.texture_day.use(location=1)
        self.texture_night.use(location=2)
        self.texture_clouds.use(location=3)
        self.sphere.render(self.program)
