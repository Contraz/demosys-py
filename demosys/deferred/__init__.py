import os

from demosys.conf import settings

settings.add_program_dir(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'programs')
)

from .renderer import DeferredRenderer  # noqa
