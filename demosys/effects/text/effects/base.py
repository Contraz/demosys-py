from demosys.effects import Effect


class FontMeta:
    """Font metadata"""
    def __init__(self, meta):
        self._meta = meta
        self.characters = self._meta['characters']
        self.character_ranges = self._meta['character_ranges']
        self.character_height = self._meta['character_height']
        self.character_width = self._meta['character_width']
        self.atlas_height = self._meta['atlas_height']
        self.atlas_width = self._meta['atlas_width']

    @property
    def char_aspect_wh(self):
        return self.character_width / self.character_height

    def char_aspect_hw(self):
        return self.character_height / self.character_width


class BaseText(Effect):
    runnable = False

    def __init__(self):
        self._meta = None
        self._ct = None

    def draw(self, *args, **kwargs):
        raise NotImplementedError()

    def _translate_string(self, data, length):
        """Translate string into character texture positions"""
        for index, char in enumerate(data):
            if index == length:
                break

            yield self._meta.characters - 1 - self._ct[char]

    def _init(self, meta: FontMeta):
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
