from demosys.loaders.base import BaseLoader
from demosys.opengl import ShaderProgram


class Loader(BaseLoader):
    name = 'single'

    def load(self):
        self.meta.resolved_path = self.find_program(self.meta.path)
        if not self.meta.resolved_path:
            raise ValueError("Cannot find program '{}'".format(self.meta.path))

        # Load it
        program = ShaderProgram(self.meta.path)

        with open(self.meta.resolved_path, 'r') as fd:
            program.set_source(fd.read())

        program.prepare()

        return program
