"""
Wrapper for a loaded scene with properties.
"""
from demosys import context, geometry
from demosys.resources import shaders
from pyrr import matrix44, vector3

from .shaders import ColorShader, FallbackShader, MeshShader, TextureShader


class Scene:
    """Generic scene"""
    def __init__(self, name, mesh_shaders=None, **kwargs):
        """
        :param name: Unique name or path for the scene
        :param loader: Loader class for the scene if relevant
        """
        self.name = name
        self.root_nodes = []

        # References resources in the scene
        self.nodes = []
        self.materials = []
        self.meshes = []
        self.cameras = []
        self.mesh_shaders = mesh_shaders or [ColorShader(), TextureShader(), FallbackShader()]

        self.bbox_min = None
        self.bbox_max = None
        self.diagonal_size = 1.0

        self.bbox_vao = geometry.bbox()
        self.bbox_shader = shaders.load('scene_default/bbox.glsl')

        self._view_matrix = matrix44.create_identity()

    @property
    def ctx(self):
        return context.ctx()

    @property
    def view_matrix(self):
        return self._view_matrix

    @view_matrix.setter
    def view_matrix(self, value):
        self._view_matrix = value.astype('f4')
        for node in self.root_nodes:
            node.calc_view_mat(self._view_matrix)

    def draw(self, projection_matrix=None, camera_matrix=None, time=0):
        """
        Draw all the nodes in the scene

        :param projection_matrix: projection matrix (bytes)
        :param camera_matrix: camera_matrix (bytes)
        :param time: The current time
        """
        projection_matrix = projection_matrix.astype('f4').tobytes()
        camera_matrix = camera_matrix.astype('f4').tobytes()

        for node in self.root_nodes:
            node.draw(
                projection_matrix=projection_matrix,
                camera_matrix=camera_matrix,
                time=time,
            )

        self.ctx.clear_samplers(0, 4)

    def draw_bbox(self, projection_matrix=None, camera_matrix=None, all=True):
        """Draw scene and mesh bounding boxes"""
        projection_matrix = projection_matrix.astype('f4').tobytes()
        camera_matrix = camera_matrix.astype('f4').tobytes()

        # Scene bounding box
        self.bbox_shader.uniform("m_proj", projection_matrix)
        self.bbox_shader.uniform("m_view", self._view_matrix.astype('f4').tobytes())
        self.bbox_shader.uniform("m_view", camera_matrix)
        self.bbox_shader.uniform("bb_min", self.bbox_min.astype('f4').tobytes())
        self.bbox_shader.uniform("bb_max", self.bbox_max.astype('f4').tobytes())
        self.bbox_shader.uniform("color", (1.0, 0.0, 0.0))
        self.bbox_vao.draw(self.bbox_shader)

        if not all:
            return

        # Draw bounding box for children
        for node in self.root_nodes:
            node.draw_bbox(projection_matrix, camera_matrix, self.bbox_shader, self.bbox_vao)

    def apply_mesh_shaders(self):
        """Applies mesh shaders to meshes"""
        if self.mesh_shaders is None:
            return

        for mesh in self.meshes:
            for ms in self.mesh_shaders:
                instance = ms.apply(mesh)
                if instance is not None:
                    if isinstance(instance, MeshShader):
                        mesh.mesh_shader = ms
                        break
                    else:
                        raise ValueError("apply() must return a MeshShader instance, not {}".format(type(instance)))
            if not mesh.mesh_shader:
                print("WARING: No mesh shader applied to '{}'".format(mesh.name))

    def calc_scene_bbox(self):
        """Calculate scene bbox"""
        bbox_min, bbox_max = None, None
        for node in self.root_nodes:
            bbox_min, bbox_max = node.calc_global_bbox(
                matrix44.create_identity(),
                bbox_min,
                bbox_max
            )

        self.bbox_min = bbox_min
        self.bbox_max = bbox_max

        self.diagonal_size = vector3.length(self.bbox_max - self.bbox_min)

    def load(self, loader, path):
        """Deferred loading if a loader is specified"""
        loader.load(self, path=path)
        self.apply_mesh_shaders()
        self.view_matrix = matrix44.create_identity()

    def destroy(self):
        """Destroy the scene data and deallocate buffers"""
        for mesh in self.meshes:
            mesh.vao.release()

    def __str__(self):
        return "<Scene: {}>".format(self.name)

    def __repr__(self):
        return str(self)
