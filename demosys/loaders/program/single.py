from demosys.loaders.base import BaseLoader
from demosys.opengl import program


class Loader(BaseLoader):
    name = 'single'

    def load(self):
        self.meta.resolved_path = self.find_program(self.meta.path)
        if not self.meta.resolved_path:
            raise ValueError("Cannot find program '{}'".format(self.meta.path))

        print("Loading:", self.meta.path)

        with open(self.meta.resolved_path, 'r') as fd:
            shaders = program.ProgramShaders.from_single(self.meta, fd.read())

        prog = shaders.create()

        # Wrap the program if reloadable is set
        if self.meta.reloadable:
            # Disable reload flag so reloads will return Program instances
            self.meta.reloadable = False
            # Wrap it ..
            prog = program.ReloadableProgram(self.meta, prog)

        return prog
