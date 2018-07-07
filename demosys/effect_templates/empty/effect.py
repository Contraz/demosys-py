from demosys.effects import effect


class Empty(effect.Effect):

    def __init__(self):
        pass

    @effect.bind_target
    def draw(self, time, frametime, target):
        pass
