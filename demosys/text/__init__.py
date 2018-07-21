import os
from demosys.conf import settings

from .writer_2d import TextWriter2D  # noqa
from .renderer_2d import TextRenderer2D  # noqa


settings.add_shader_dir(os.path.join(os.path.dirname(__file__), 'shaders'))
