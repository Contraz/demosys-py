

class Context:

    def __init__(self, width=0, height=0):
        # window size
        self.width = width
        self.height = height
        # Actual window buffer size. Needs adjustment for retina and 4k resolution by child
        self.buffer_width = width
        self.buffer_height = height
        # ModernGL context
        self.ctx = None

    def swap_buffers(self):
        """Swap frame buffer"""
        raise NotImplementedError()

    def resize(self, width, height):
        """Resize window"""
        raise NotImplementedError()

    def close(self):
        """Hits the window to close"""
        raise NotImplementedError()

    def should_close(self):
        """Check if window should close"""
        raise NotImplementedError()

    def terminate(self):
        raise NotImplementedError()
