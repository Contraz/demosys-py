"""
Text writer using monospace font from texture
"""
from demosys import context


class BaseText:
    """
    Base class assigning context
    """

    def __init__(self):
        self.ctx = context.ctx()

    def draw(self, *args, **kwargs):
        raise NotImplementedError()
