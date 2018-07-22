import os
from demosys.conf import settings

from .writer2d import TextWriter2D  # noqa
from .renderer2d import TextRenderer2D  # noqa

# Register resource paths
settings.add_shader_dir(os.path.join(os.path.dirname(__file__), 'resources', 'shaders'))
settings.add_texture_dir(os.path.join(os.path.dirname(__file__), 'resources', 'textures'))
settings.add_data_dir(os.path.join(os.path.dirname(__file__), 'resources', 'data'))
