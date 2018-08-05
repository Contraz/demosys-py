from demosys import context


class BaseLoader:
    name = None

    def __init__(self, path, **kwargs):
        self.path = path
        self.kwargs = kwargs

    def load(self):
        pass

    @property
    def ctx(self):
        return context.ctx()
