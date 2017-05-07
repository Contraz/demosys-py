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

    def key_event(self, key, scancode, action, mods):
        """
        Forwarded (unconsumed) key events from the system.
        See glfw's key events for detailed information.

        :param key: The keyboard key that was pressed or released.
        :param scancode: The system-specific scancode of the key.
        :param action: GLFW_PRESS, GLFW_RELEASE or GLFW_REPEAT
        :param mods: Bit field describing which modifier keys were held down.
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

        # If an effect was specified in the initializer, find it
        if self.effect_module:
            for effect in effect_list:
                if effect.name == self.effect_module:
                    self.active_effect = effect
        else:
            # Otherwise we look just grab the first effect
            self.active_effect = effect_list[0]

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

    def key_event(self, key, scancode, action, mods):
        # print("SingleEffectManager:key_event", key, scancode, action, mods)
        pass


class TrackerEffectManager(BaseEffectManger):
    """Effect manager handling tracker data"""
    pass
