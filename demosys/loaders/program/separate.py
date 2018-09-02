from demosys.loaders.base import BaseLoader
from demosys.opengl import program


class Loader(BaseLoader):
    name = 'separate'

    def load(self):
        vs_source = self.load_shader("vertex", self.meta.vertex_shader)
        geo_source = self.load_shader("geometry", self.meta.geometry_shader)
        fs_source = self.load_shader("fragment", self.meta.fragment_shader)
        tc_source = self.load_shader("tess_control", self.meta.tess_control_shader)
        te_source = self.load_shader("tess_evaluation", self.meta.tess_evaluation_shader)

        shaders = program.ProgramShaders.from_separate(
            self.meta,
            vs_source,
            geometry_source=geo_source,
            fragment_source=fs_source,
            tess_control_source=tc_source,
            tess_evaluation_source=te_source,
        )
        prog = shaders.create()

        # Wrap the program if reloadable is set
        if self.meta.reloadable:
            # Disable reload flag so reloads will return Program instances
            self.meta.reloadable = False
            # Wrap it ..
            prog = program.ReloadableProgram(self.meta, prog)

        return prog

    def load_shader(self, shader_type: str, path: str):
        """Load a single shader"""
        if path:
            resolved_path = self.find_program(path)
            if not resolved_path:
                raise ValueError("Cannot find {} shader '{}'".format(shader_type, path))

            print("Loading:", path)

            with open(resolved_path, 'r') as fd:
                return fd.read()
