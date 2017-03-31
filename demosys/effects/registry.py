import os
import importlib
import inspect
from demosys.effects.effect import Effect

EFFECT_MODULE = 'effect'


class EffectConfig:
    def __init__(self, module=None, cls=None):
        self.module = module
        self.cls = cls
        self.name = module.__name__
        self.path = os.path.dirname(module.__file__)


class Effects:
    """
    Registry for effects.
    This also collects what resources effects are using
    so we can use this in resource loading later on.
    """
    def __init__(self):
        self.effects = {}

    def get_effects(self):
        """Get all effect classes"""
        for name, config in self.effects.items():
            yield config.cls(name=name.replace(f".{EFFECT_MODULE}", ''))

    def get_dirs(self):
        """Get all effect directories"""
        for k, v in self.effects.items():
            yield v.path

    def polulate(self, effect_list):
        """
        Load all effects
        """
        for effect in effect_list:
            module = importlib.import_module(f'{effect}.{EFFECT_MODULE}')
            # Find the Effect class in the module
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj):
                    if obj == Effect:
                        continue
                    # Use MRO to figure out if this is really an effect
                    mro = inspect.getmro(obj)
                    if obj in mro and Effect in mro:
                        self.effects[module.__name__] = EffectConfig(module=module, cls=obj)


effects = Effects()
