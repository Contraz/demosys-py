

class BaseTimeline:
    """
    Base effect manager.
    A manager is responsible for figuring out what effect should be drawn
    at any given time.
    """
    def __init__(self, project, **kwargs):
        self._project = project

    def get_active_effect(self, time):
        raise NotImplementedError()

    def draw(self, time, frametime, target):
        """
        Called by the system every frame.
        This method should be overridden.

        :param time: The current time in seconds
        :param frametime: The time one frame should take in seconds
        :param target: The target FBO
        """
        raise NotImplementedError()

    def key_event(self, key, scancode, action, mods):
        """
        Forwarded (unconsumed) key events from the system.
        See glfw's key events for detailed information.

        :param key: The keyboard key that was pressed or released.
        :param scancode: The system-specific scancode of the key.
        :param action: GLFW_PRESS, GLFW_RELEASE or GLFW_REPEAT
        :param mods: Bit field describing which modifier keys were held down.
        """
        raise NotImplementedError()
