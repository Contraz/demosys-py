

class BaseTimer:
    """
    The base class guiding the implementation of timers.
    All methods must be implemented.
    """
    def __init__(self, **kwargs):
        pass

    def start(self):
        """
        Start the timer initially or resume after pause

        Raises:
            NotImplementedError
        """
        raise NotImplementedError()

    def pause(self):
        """
        Pause the timer

        Raises:
            NotImplementedError
        """
        raise NotImplementedError()

    def toggle_pause(self):
        """
        Toggle pause state

        Raises:
            NotImplementedError
        """
        raise NotImplementedError()

    def stop(self) -> float:
        """
        Stop the timer. Should only be called once when stopping the timer.

        Returns:
            The time the timer was stopped

        Raises:
            NotImplementedError
        """
        raise NotImplementedError()

    def get_time(self) -> float:
        """
        Get the current time in seconds

        Returns:
            The current time in seconds

        Raises:
            NotImplementedError
        """
        raise NotImplementedError()

    def set_time(self, value: float):
        """
        Set the current time in seconds.

        Args:
            value (float): The new time

        Raises:
            NotImplementedError
        """
        raise NotImplementedError()
