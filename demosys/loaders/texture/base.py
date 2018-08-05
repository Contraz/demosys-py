from demosys import context


class BaseLoader:
    name = None

    def __init__(self, path):
        self.path = path

    def ctx(self):
        return context.ctx()

    def load(self):
        pass
