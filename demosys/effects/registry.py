import importlib
import inspect
import os
from typing import Any, List, Type

from demosys.effects.effect import Effect


class Effects:
    """
    Registry for effects classes (not instances).

    It collects all effects in registed effect modules
    and shares information about them to the system.
    """
    def __init__(self):
        self.packages = []
        # EffectPackages with package path as key
        self.package_map = {}

    def get_dirs(self) -> List[str]:
        """
        Get all effect directories for registered effects.
        """
        for package in self.packages:
            yield os.path.join(package.path, 'resources')

    def get_effect_resources(self) -> List[Any]:
        """
        Get all resources registed in effect packages.
        These are typically located in ``resources.py``
        """
        resources = []
        for package in self.packages:
            resources.extend(package.resources)

        return resources

    def polulate(self, package_list):
        """
        Polulate the registry with effect packges.
        This is normally the ``settings.EFFECTS`` list

        :param module_list: List of effect module paths
        """
        for package in package_list:
            self.add_package(package)

    def add_package(self, name):
        """
        Registers a single package

        :param name: (str) The effect package to add
        """
        package = EffectPackage(name)
        package.load()

        self.packages.append(package)
        self.package_map[package.path] = package

    def get_package(self, name) -> 'EffectPackage':
        """
        Get a package by python path
        """
        try:
            return self.package_map[name]
        except KeyError:
            raise EffectError("No package '{}' registered".format(name))

    def find_effect_class(self, class_name, package_name=None) -> Type[Effect]:
        if package_name:
            package = self.get_package(package_name)
            return package.find_effect_class(class_name, raise_for_error=True)

        for package in self.packages:
            effect_cls = package.find_effect_class(class_name)
            if effect_cls:
                return effect_cls

        raise EffectError("No effect class '{}' found in any packages".format(effect_cls))


class EffectPackage:
    """Loads and stores information about an effect package"""

    def __init__(self, name):
        self.name = name
        self.package = None

        self.effect_module = None
        self.effect_classes = None
        self.effect_class_map = {}

        self.resource_description_module = None
        self.resources = []

    def runnable_effects(self) -> List[Type[Effect]]:
        """Returns the first runnable effect in the package"""
        return [cls for cls in self.effect_classes if cls.runnable]

    def find_effect_class(self, class_name, raise_for_error=False) -> Type[Effect]:
        try:
            return self.effect_class_map[class_name]
        except KeyError:
            raise EffectError("No effect class '{}' found in package '{}'".format(class_name, self.name))

    @property
    def path(self) -> str:
        return self.package.__path__._path[0]

    @property
    def effect_module_name(self) -> str:
        return self.effect_module.__name__

    def load(self):
        self.load_package()
        self.load_effect_module()
        self.load_effects_classes()
        self.load_resource_module()

    def load_package(self):
        """FInd the effect package"""
        try:
            self.package = importlib.import_module(self.name)
        except ModuleNotFoundError:
            raise ModuleNotFoundError("Effect package '{}' not found.".format(self.name))

    def load_effect_module(self):
        """Attempt to load the effect module"""
        self.load_effect_module_old()
        if not self.effect_module:
            self.load_effect_module_new()

    def load_effect_module_old(self):
        """Attempt to load the old effect module"""
        try:
            name = '{}.{}'.format(self.name, 'effect')
            self.effect_module = importlib.import_module(name)
            print("Warning: Effect module name 'effect' should be renamed to 'effects'")
        except ModuleNotFoundError:
            pass

    def load_effect_module_new(self):
        try:
            name = '{}.{}'.format(self.name, 'effects')
            self.effect_module = importlib.import_module(name)
        except ModuleNotFoundError:
            raise EffectError("Effect package '{}' has no effect module".format(self.name))

    def load_effects_classes(self):
        """Iterate the module attributes picking out effects"""
        self.effect_classes = []

        for _, cls in inspect.getmembers(self.effect_module):
            if inspect.isclass(cls):
                if cls == Effect:
                    continue

                if issubclass(cls, Effect):
                    self.effect_classes.append(cls)
                    self.effect_class_map[cls.__name__] = cls

    def load_resource_module(self):
        """Fetch the resource list"""
        # Do we have a resources folder?
        if not os.path.exists(os.path.join(self.path, 'resources')):
            return

        # Attempt to load resource descriptions
        try:
            name = '{}.{}'.format(self.name, 'resources.descriptions')
            self.resource_description_module = importlib.import_module(name)
        except ModuleNotFoundError:
            raise EffectError("Effect package '{}' has no resources module".format(self.name))

        try:
            self.resources = getattr(self.resource_description_module, 'resources')
        except KeyError:
            raise EffectError("Effect resource module '{}' has no resources attribute".format(name))


class EffectError(Exception):
    pass


effects = Effects()
