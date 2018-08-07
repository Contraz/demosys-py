from demosys.loaders.base import BaseLoader


class Loader(BaseLoader):
    name = 'single'

    def load(self):
        return "Hello!"
