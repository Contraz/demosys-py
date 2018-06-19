

class Material:
    def __init__(self, name):
        self.name = name
        self.color = None
        self.mat_texture = None
        self.double_sided = True


class MaterialTexture:
    def __init__(self, texture=None, sampler=None):
        self.texture = texture
        self.sampler = sampler
