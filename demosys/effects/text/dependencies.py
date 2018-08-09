from demosys.resources.meta import TextureDescription, ProgramDescription, DataDescription

effect_packages = []

resources = [
    # Font meta and texture
    DataDescription(
        label='demosys.program.font_meta',
        path='demosys/text/meta.json', loader='json',
    ),
    TextureDescription(
        label='demosys.text.font_texture',
        path='demosys/text/VeraMono.png',
        loader='array',
        layers=190,
        mipmap=True,
    ),

    # Textwriter shader
    ProgramDescription(
        label='demosys.text.program_writer_2d',
        path='demosys/text/textwriter2d.glsl',
    ),

    # TextRenderer shader
    ProgramDescription(
        label='demosys.text.program_renderer_2d',
        path='demosys/text/view_renderer_texture.glsl',
    ),
]
