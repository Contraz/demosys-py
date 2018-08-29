import sys
from unittest.mock import MagicMock

MOCK_MODULES = [
    'glfw',
    'pyglet',
    'pyglet.window',
]


def apply_mocks():
    class Mock(MagicMock):
        @classmethod
        def __getattr__(cls, name):
            return MagicMock()

    sys.modules.update((mod_name, Mock()) for mod_name in MOCK_MODULES)
