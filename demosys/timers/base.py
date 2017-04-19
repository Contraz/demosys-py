

class BaseTimer:
    """Timer based on glfw time"""
    def __init__(self, **kwargs):
        pass

    def start(self):
        """Start the timer"""
        raise NotImplemented

    def pause(self):
        """Pause the timer"""
        raise NotImplemented

    def toggle_pause(self):
        """Toggle pause"""
        raise NotImplemented

    def stop(self):
        """Stop the timer"""
        raise NotImplemented

    def get_time(self):
        """Get the current time in seconds (float)"""
        raise NotImplemented
