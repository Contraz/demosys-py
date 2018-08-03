import os

from demosys.conf import settings

settings.add_shader_dir(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'shaders')
)

from .renderer import DeferredRenderer  # noqa
