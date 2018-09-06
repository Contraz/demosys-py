import importlib
import inspect
import os
from typing import Any, List, Type

from demosys.effects.effect import Effect


def parse_package_string(path):
    """
    Parse the effect package string.
    Can contain the package python path or path to effect class in an effect package.

    Examples::

        # Path to effect pacakge
        examples.cubes

        # Path to effect class
        examples.cubes.Cubes

    Args:
        path: python path to effect package. May also include effect class name.

    Returns:
        tuple: (package_path, effect_class)
    """
    parts = path.split('.')

    # Is the last entry in the path capitalized?
    if parts[-1][0].isupper():
        return ".".join(parts[:-1]), parts[-1]

    return path, ""


class EffectRegistry:
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
        Polulate the registry with effect packages.

        :param module_list: List of effect module paths
        """
        for package in package_list:
            self.add_package(package)

    def add_package(self, name):
        """
        Registers a single package

        :param name: (str) The effect package to add
        """
        name, cls_name = parse_package_string(name)

        if name in self.package_map:
            return

        package = EffectPackage(name)
        package.load()

        self.packages.append(package)
        self.package_map[package.name] = package

        # Load effect package dependencies
        self.polulate(package.effect_packages)

    def get_package(self, name) -> 'EffectPackage':
        """
        Get a package by python path. Can also contain path to an effect.

        Args:
            name (str): Path to effect package or effect

        Returns:
            The requested EffectPackage

        Raises:
            EffectError when no package is found
        """
        name, cls_name = parse_package_string(name)

        try:
            return self.package_map[name]
        except KeyError:
            raise EffectError("No package '{}' registered".format(name))

    def find_effect_class(self, path) -> Type[Effect]:
        """
        Find an effect class by class name or full python path to class

        Args:
            path (str): effect class name or full python path to effect class

        Returns:
            Effect class

        Raises:
            EffectError if no class is found
        """
        package_name, class_name = parse_package_string(path)

        if package_name:
            package = self.get_package(package_name)
            return package.find_effect_class(class_name, raise_for_error=True)

        for package in self.packages:
            effect_cls = package.find_effect_class(class_name)
            if effect_cls:
                return effect_cls

        raise EffectError("No effect class '{}' found in any packages".format(class_name))


class EffectPackage:
    """Loads and stores information about an effect package"""

    def __init__(self, name):
        self.name = name
        self.package = None

        self.effect_module = None
        self.effect_classes = None
        self.effect_class_map = {}

        self.dependencies_module = None
        self.resources = []
        self.effect_packages = []

    def runnable_effects(self) -> List[Type[Effect]]:
        """Returns the runnable effect in the package"""
        return [cls for cls in self.effect_classes if cls.runnable]

    def find_effect_class(self, class_name, raise_for_error=False) -> Type[Effect]:
        try:
            return self.effect_class_map[class_name]
        except KeyError:
            if raise_for_error:
                raise EffectError("No effect class '{}' found in package '{}'".format(class_name, self.name))

        return None

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
        try:
            name = '{}.{}'.format(self.name, 'effects')
            self.effect_module = importlib.import_module(name)
        except ModuleNotFoundError as err:
            raise EffectError(
                (
                    "Failed to import effects module '{}'.\n"
                    "This means the module doesn't exist "
                    "or you have an import errors inside the effects module.\n\n"
                    "Forwarded error from importlib: {}\n"
                ).format(self.name, err))

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
                    cls._name = "{}.{}".format(self.effect_module_name, cls.__name__)

    def load_resource_module(self):
        """Fetch the resource list"""
        # Attempt to load the dependencies module
        try:
            name = '{}.{}'.format(self.name, 'dependencies')
            self.dependencies_module = importlib.import_module(name)
        except ModuleNotFoundError as err:
            raise EffectError(
                (
                    "Effect package '{}' has no 'dependencies' module or the module has errors. "
                    "Forwarded error from importlib: {}"
                ).format(self.name, err))

        # Fetch the resource descriptions
        try:
            self.resources = getattr(self.dependencies_module, 'resources')
        except AttributeError:
            raise EffectError("Effect dependencies module '{}' has no 'resources' attribute".format(name))

        if not isinstance(self.resources, list):
            raise EffectError(
                "Effect dependencies module '{}': 'resources' is of type {} instead of a list".format(
                    name, type(self.resources)))

        # Fetch the effect class list
        try:
            self.effect_packages = getattr(self.dependencies_module, 'effect_packages')
        except AttributeError:
            raise EffectError("Effect dependencies module '{}' has 'effect_packages' attribute".format(name))

        if not isinstance(self.effect_packages, list):
            raise EffectError(
                "Effect dependencies module '{}': 'effect_packages' is of type {} instead of a list".format(
                    name, type(self.effects)))

    def __str__(self):
        return "<{} {}>".format(self.__class__.__name__, self.name)

    def __repr__(self):
        return str(self)


class EffectError(Exception):
    pass


effects = EffectRegistry()
