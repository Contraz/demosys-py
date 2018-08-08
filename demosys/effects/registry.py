import importlib
import inspect
import os

from demosys.effects.effect import Effect


class Effects:
    """
    Registry for effects classes (not instances).

    It collects all effects in registed effect modules
    and shares information about them to the system.
    """
    def __init__(self):
        self.packages = []
        self.effect_classes = {}

    def get_dirs(self):
        """
        Get all effect directories for registered effects.
        """
        for package in self.packages:
            yield package.package_path

    def get_effect_resources(self):
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

    def add_package(self, package_name):
        """
        Registers a single package

        :param package_name: (str) The effect package to add
        """
        package = EffectPackage(package_name)
        package.load()
        self.packages.append(package)


class EffectPackage:
    """Loads and stores information about an effect package"""

    def __init__(self, package_name):
        self.package_name = package_name
        self.package = None

        self.effect_module = None
        self.effect_classes = None

        self.resource_module = None
        self.resources = None

    @property
    def package_path(self):
        return self.package.__path__

    @property
    def effect_module_name(self):
        return self.effect_module.__name__

    def load(self):
        self.load_package()
        self.load_effect_module()
        self.load_effects_classes()
        self.load_resource_module()

    def load_package(self):
        """FInd the effect package"""
        try:
            self.package = importlib.import_module(self.package_name)
        except ModuleNotFoundError:
            raise ModuleNotFoundError("Effect package '{}' not found.".format(self.package_name))

    def load_effect_module(self):
        """Attempt to load the effect module"""
        self.load_effect_module_old()
        if not self.effect_module:
            self.load_effect_module_new()

    def load_effect_module_old(self):
        """Attempt to load the old effect module"""
        try:
            name = '{}.{}'.format(self.package_name, 'effect')
            self.effect_module = importlib.import_module(name)
            print("Warning: Effect module name 'effect' should be renamed to 'effects'")
        except ModuleNotFoundError:
            pass

    def load_effect_module_new(self):
        try:
            name = '{}.{}'.format(self.package_name, 'effects')
            self.effect_module = importlib.import_module(name)
        except ModuleNotFoundError:
            raise EffectError("Effect package '{}' has no effect module".format(self.package_name))

    def load_effects_classes(self):
        """Iterate the module attributes picking out effects"""
        self.effect_classes = []

        for _, cls in inspect.getmembers(self.effect_module):
            if inspect.isclass(cls):
                if cls == Effect:
                    continue

                if issubclass(cls, Effect):
                    self.effect_classes.append(cls)


    def load_resource_module(self):
        """Fetch the resource list"""
        try:
            name = '{}.{}'.format(self.package_name, 'resources')
            self.resource_module = importlib.import_module(name)
        except ModuleNotFoundError:
            raise EffectError("Effect package '{}' has no resource module".format(self.package_name))

        try:
            self.resources = getattr(self.resource_module, 'resources')
        except KeyError:
            raise EffectError("Effect resource module '{}' has no resources attribute".format(name))


class EffectError(Exception):
    pass


effects = Effects()
