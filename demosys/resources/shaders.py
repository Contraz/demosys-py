"""Shader Registry"""
from demosys.opengl import Shader
from demosys.core.shaderfiles.finders import get_finders
from demosys.core.exceptions import ImproperlyConfigured


class Shaders:
    def __init__(self):
        self.shaders = {}

    @property
    def count(self):
        return len(self.shaders)

    def get(self, path, create=False):
        shader = self.shaders.get(path)
        if create and not shader:
            shader = Shader(path)
            self.shaders[path] = shader
        return shader

    def load(self):
        finders = list(get_finders())
        print("Loading shaders:")
        for name, shader in self.shaders.items():
            for finder in finders:
                path = finder.find(name)
                if path:
                    print(" - {}".format(path))
                    shader.set_source(open(path, 'r').read())
                    shader.prepare()
                    break
            else:
                raise ImproperlyConfigured("Cannot find shader {}".format(name))


shaders = Shaders()
