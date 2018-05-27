"""
Wrapper for a loaded scene with properties.
"""


class Scene:
    """Generic scene"""
    def __init__(self, name, loader=None, **kwargs):
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

    def draw(self, m_mv, m_proj, shader):
        for node in self.root_nodes:
            node.draw(m_mv, m_proj, shader)

    def load(self, path):
        """Deferred loading if a loader is specified"""
        if not hasattr(self, 'loader'):
            return

        if self.loader:
            self.loader.load(self, file=path)

    def __str__(self):
        return "<Scene: {}>".format(self.name)

    def __repr__(self):
        return str(self)
