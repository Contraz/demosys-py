from demosys.effects.registry import effects


class ManagerError(Exception):
    pass


class BaseEffectManger:
    """
    Base effect manager.
    A manager is responsible for figuring out what effect should be drawn
    at any given time.
    """
    def pre_load(self):
        """
        Called after OpenGL context creation before resources are loaded.
        This method should be overridden.
        """
        return True

    def post_load(self):
        """
        Called after resources are loaded.
        This method should be overridden.
        """
        return True

    def draw(self, time, frametime, target):
        """
        Called by the system every frame.
        This method should be overridden.

        :param time: The current time in seconds
        :param frametime: The time one frame should take in seconds
        :param target: The target FBO
        """
        pass


class SingleEffectManager(BaseEffectManger):
    """Run a single effect"""
    def __init__(self, effect_module=None):
        """
        Initalize the manager telling it what effect should run.

        :param effect_module: The effect module to run
        """
        self.active_effect = None
        self.effect_module = effect_module

    def pre_load(self):
        """
        Initialize the effect that should run.
        """
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
