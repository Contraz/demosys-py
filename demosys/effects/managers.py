from demosys.effects.registry import effects


class ManagerError(Exception):
    pass


class BaseEffectManger:
    """Base effect manager"""
    def __init__(self, *args, **kwargs):
        pass

    def init_effects(self):
        """Init after context creations"""
        pass

    def draw(self, time, target):
        """Draw efffect(s)"""
        pass


class SingleEffectManager(BaseEffectManger):
    """Run a single effect"""
    def __init__(self, effect_module=None):
        self.active_effect = None
        self.effect_module = effect_module
        super().__init__()

    def init_effects(self):
        """Init after context creations"""
        effect_list = [cls for cls in effects.get_effects()]
        for effect in effect_list:
            effect.init()
            if effect.name == self.effect_module:
                self.active_effect = effect

        if not self.active_effect:
            print("Cannot find effect '{}'".format(self.active_effect))
            print("Available effects:")
            print("\n".join(e.name for e in effect_list))
            return False
        return True

    def draw(self, time, target):
        self.active_effect.draw(time, target)


class TrackerEffectManager(BaseEffectManger):
    """Effect manager handling tracker data"""
    pass
