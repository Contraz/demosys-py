import moderngl as mgl
from demosys.effects import effect


class SceneEffect(effect.Effect):
    """Generated default effect"""
    def __init__(self):
        self.scene = self.get_scene("Sponza/glTF/Sponza.gltf", local=True)

        self.proj_mat = self.create_projection(fov=75.0, near=0.01, far=1000.0)

    @effect.bind_target
    def draw(self, time, frametime, target):
        self.ctx.enable(mgl.DEPTH_TEST)
        self.sys_camera.velocity = self.scene.diagonal_size / 5.0

        self.scene.draw(
            projection_matrix=self.proj_mat,
            camera_matrix=self.sys_camera.view_matrix,
            time=time,
        )

        # Draw bbox
        # self.scene.draw_bbox(self.proj_mat, self.sys_camera.view_matrix, all=True)
