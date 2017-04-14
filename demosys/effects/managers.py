from demosys.effects.registry import effects


class ManagerError(Exception):
    pass


class BaseEffectManger:
    """Base effect manager"""
    def pre_load(self):
        """Init after context creations"""
        return True

    def post_load(self):
        return True

    def draw(self, time, frametime, target):
        """Draw efffect(s)"""
        pass


class SingleEffectManager(BaseEffectManger):
    """Run a single effect"""
    def __init__(self, effect_module=None):
        self.active_effect = None
        self.effect_module = effect_module

    def pre_load(self):
        """Init after context creations"""
        effect_list = [cfg.cls() for name, cfg in effects.effects.items()]
        for effect in effect_list:
            if effect.name == self.effect_module:
                self.active_effect = effect

        if not self.active_effect:
            print("Cannot find effect '{}'".format(self.active_effect))
            print("Available effects:")
            print("\n".join(e.name for e in effect_list))
            return False
        return True

    def post_load(self):
        return True

    def draw(self, time, frametime, target):
        self.active_effect.draw(time, frametime, target)


class TrackerEffectManager(BaseEffectManger):
    """Effect manager handling tracker data"""
    pass
