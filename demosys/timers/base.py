

class BaseTimer:
    """Timer based on glfw time"""
    def __init__(self, **kwargs):
        pass

    def start(self):
        """Start the timer"""
        raise NotImplementedError()

    def pause(self):
        """Pause the timer"""
        raise NotImplementedError()

    def toggle_pause(self):
        """Toggle pause"""
        raise NotImplementedError()

    def stop(self):
        """Stop the timer"""
        raise NotImplementedError()

    def get_time(self):
        """Get the current time in seconds (float)"""
        raise NotImplementedError()
