import moderngl as mgl
from demosys.effects import effect
from pyrr import matrix44


class SceneEffect(effect.Effect):
    """Generated default effect"""
    def __init__(self):
        self.scene = self.get_scene("Sponza/glTF/Sponza.gltf", local=True)

        self.proj_mat = self.create_projection(fov=75.0, near=0.01, far=1000.0)

    @effect.bind_target
    def draw(self, time, frametime, target):
        self.ctx.enable(mgl.DEPTH_TEST)
        self.sys_camera.velocity = self.scene.diagonal_size / 5.0

        # Rotate and translate
        # m_mv = self.create_transformation(rotation=(time * 1.2, time * 2.1, time * 0.25),
        #                                   translation=(0.0, 0.0, -2.0))
        # m_mv = self.create_transformation(
        #     rotation=(0.0, 3.14, 0.0),
        #     translation=(0.0, 0.0, 0.0))
        # view_mat = matrix44.create_identity(dtype='f4')
        self.scene.draw(self.proj_mat, self.sys_camera.view_matrix, time=time)

        # Draw bbox
        # self.scene.draw_bbox(self.m_proj, m_mv, all=True)
