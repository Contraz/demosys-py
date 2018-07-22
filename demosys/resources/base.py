"""
Base registry class
"""


class BaseRegistry:
    """
    Base registry class providing callback functionality
    for each registry type.
    """

    def __init__(self):
        self._on_loaded_funcs = []

    def on_loaded(self, func):
        """Register functions to call when all data is loaded"""
        self._on_loaded_funcs.append(func)

    def _on_loaded(self):
        for func in self._on_loaded_funcs:
            func()
