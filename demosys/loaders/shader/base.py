from demosys import context


class ShaderLoader:
    name = None

    def __init__(self):
        pass

    @property
    def ctx(self):
        return context.ctx()

    def load(self):
        pass
