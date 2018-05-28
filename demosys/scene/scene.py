"""
Wrapper for a loaded scene with properties.
"""
from .shaders import MeshShader


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
        self.mesh_shaders = mesh_shaders or []

    def draw(self, m_mv, m_proj):
        for node in self.root_nodes:
            node.draw(m_mv, m_proj)

    def apply_mesh_shaders(self, mesh_shaders):
        """Applies mesh shaders to meshes"""
        if mesh_shaders is None:
            return

        for mesh in self.meshes:
            for ms in mesh_shaders:
                instance = ms.apply(mesh)
                if instance is not None:
                    if isinstance(instance, MeshShader):
                        mesh.mesh_shader = ms
                        continue
                    else:
                        raise ValueError("apply() must return a MeshShader instance, not {}".format(type(instance)))
            else:
                print("WARING: No mesh shader applied to '{}'".format(mesh.name))

    def load(self, path):
        """Deferred loading if a loader is specified"""
        if not hasattr(self, 'loader'):
            return

        if self.loader:
            self.loader.load(self, file=path)

        self.apply_mesh_shaders(self.mesh_shaders)

    def __str__(self):
        return "<Scene: {}>".format(self.name)

    def __repr__(self):
        return str(self)
