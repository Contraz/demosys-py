import os
import importlib
import inspect
from demosys.effects.effect import Effect

EFFECT_MODULE = 'effect'


class EffectError(Exception):
    pass


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

    def get_dirs(self):
        """
        Get all effect directories for registered effects.
        """
        for k, v in self.effects.items():
            yield v.path

    def polulate(self, effect_list):
        """
        Find all effect modules.

        :param effect_list: List of effect module paths
        """
        for effect in effect_list:
            name = '{}.{}'.format(effect, EFFECT_MODULE)
            module, cls = self.get_effect_cls(name)
            if cls:
                cls.name = effect
                self.effects[module.__name__] = EffectConfig(module=module, cls=cls)
            else:
                raise EffectError("Effect '{}' has no effect class".format(effect))

    def get_effect_cls(self, module_name):
        """
        Find and return an effect class in a module

        :param module_name: Name of the module
        :returns: module, cls tuple
        """
        module = importlib.import_module(module_name)

        # Find the Effect class in the module
        for name, cls in inspect.getmembers(module):
            if inspect.isclass(cls):
                if cls == Effect:
                    continue
                # Use MRO to figure out if this is really an effect
                mro = inspect.getmro(cls)
                if cls in mro and Effect in mro:
                    return module, cls

        return None, None


effects = Effects()
