"""
Text writer using monospace font from texture
"""
import json

from demosys import context


class BaseText:
    """
    Base class assigning context
    """

    def __init__(self):
        self.ctx = context.ctx()
        self._meta = None
        self._ct = None

    def draw(self, *args, **kwargs):
        raise NotImplementedError()

    def _translate_data(self, data):
        """Translate character bytes into texture positions"""
        return [self._meta.characters - 1 - self._ct[c] for c in data]

    def _init(self, meta: 'Meta'):
        self._meta = meta
        # Check if the atlas size is sane
        if not self._meta.characters * self._meta.character_height == self._meta.atlas_height:
            raise ValueError("characters * character_width != atlas_height")

        self._generate_character_map()

    def _generate_character_map(self):
        """Generate character translation map (latin1 pos to texture pos)"""
        self._ct = [-1] * 256
        index = 0
        for crange in self._meta.character_ranges:
            for cpos in range(crange['min'], crange['max'] + 1):
                self._ct[cpos] = index
                index += 1


class Meta:
    """Font metadata"""
    def __init__(self, meta):
        self._meta = json.loads(meta)
        self.characters = self._meta['characters']
        self.character_ranges = self._meta['character_ranges']
        self.character_height = self._meta['character_height']
        self.character_width = self._meta['character_width']
        self.atlas_height = self._meta['atlas_height']
        self.atlas_width = self._meta['atlas_width']
