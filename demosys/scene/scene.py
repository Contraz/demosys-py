"""
Wrapper for a loaded scene with properties.
"""
from .shaders import MeshShader, ColorShader, TextureShader, FallbackShader
from demosys import geometry
from demosys.resources import shaders
from pyrr import matrix44, vector3


class Scene:
    """Generic scene"""
    def __init__(self, name, loader=None, mesh_shaders=None, **kwargs):
        """
        :param name: Unique name or path for the scene
        :param loader: Loader class for the scene if relevant
        """
        self.name = name
        self.loader = loader
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
        self.bbox_shader = shaders.get('scene_default/bbox.glsl', create=True)

    def draw(self, m_proj, m_mv):
        for node in self.root_nodes:
            node.draw(m_proj, m_mv)

    def draw_bbox(self, m_proj, m_mv, all=True):
        """Draw scene and mesh bounding boxes"""
        # Scene bounding box
        self.bbox_shader.uniform("m_proj", m_proj.astype('f4').tobytes())
        self.bbox_shader.uniform("m_mv", m_mv.astype('f4').tobytes())
        self.bbox_shader.uniform("bb_min", self.bbox_min.astype('f4').tobytes())
        self.bbox_shader.uniform("bb_max", self.bbox_max.astype('f4').tobytes())
        self.bbox_shader.uniform("color", (1.0, 0.0, 0.0))
        self.bbox_vao.draw(self.bbox_shader)

        if not all:
            return

        # Draw bounding box for children
        for node in self.root_nodes:
            node.draw_bbox(m_proj, m_mv, self.bbox_shader, self.bbox_vao)

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

    def load(self, path):
        """Deferred loading if a loader is specified"""
        if not hasattr(self, 'loader'):
            return

        if self.loader:
            self.loader.load(self, file=path)

        self.apply_mesh_shaders()

    def __str__(self):
        return "<Scene: {}>".format(self.name)

    def __repr__(self):
        return str(self)
