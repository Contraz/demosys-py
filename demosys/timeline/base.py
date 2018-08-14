

class BaseTimeline:
    """
    Base effect manager.
    A manager is responsible for figuring out what effect should be drawn
    at any given time.
    """
    def __init__(self, project, *args, **kwargs):
        self._project = project

    def draw(self, time, frametime, target):
        """
        Called by the system every frame.
        This method should be overridden.

        :param time: The current time in seconds
        :param frametime: The time one frame should take in seconds
        :param target: The target FBO
        """
        raise NotImplementedError()

    def key_event(self, key, action, mods):
        """
        Forwarded key events from the system.

        :param key: The key that was pressed or released.
        :param action: ACTION_PRESS, ACTION_RELEASE
        :param mods: Bit field describing which modifier keys were held down.
        """
        pass
