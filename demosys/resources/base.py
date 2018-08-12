"""
Base registry class
"""
import inspect
from pathlib import Path
from typing import Any, Dict, Type

from demosys.exceptions import ImproperlyConfigured
from demosys.loaders.base import BaseLoader


class ResourceDescription:
    """
    Description of any resource.
    Resource descriptions are required by the resource system
    to load a resource.
    """
    require_label = True  # Decides if the resource requires a label
    default_loader = None  # The default loader if nothing is specified
    resource_type = None  # What resource type is described

    def __init__(self, **kwargs):
        self._kwargs = kwargs

        # All resources should have a label
        if not self.label and self.require_label:
            raise ValueError("Resource is missing label: {}".format(self.kwargs))

    @property
    def label(self) -> str:
        """
        (str) The internal label this resource is associated with
        """
        return self._kwargs.get('label')

    @property
    def path(self):
        """
        (str) The path to a resource when a single file is specified
        """
        return self._kwargs.get('path')

    @property
    def loader(self):
        """
        (str) Name of the loader
        """
        return self._kwargs.get('loader') or self.default_loader

    @loader.setter
    def loader(self, value):
        self._kwargs['loader'] = value

    @property
    def loader_cls(self) -> Type:
        """
        (Type) The loader class for this resource
        """
        return self._kwargs.get('loader_cls')

    @loader_cls.setter
    def loader_cls(self, value: Type):
        self._kwargs['loader_cls'] = value

    @property
    def resolved_path(self) -> Path:
        """
        (pathlib.Path) The resolved path by a finder
        """
        return self.kwargs.get('resolved_path')

    @resolved_path.setter
    def resolved_path(self, value: Path):
        self._kwargs['resolved_path'] = value

    @property
    def kwargs(self) -> Dict[str, str]:
        """
        (dict) All keywords arguments passed to the resource
        """
        return self._kwargs

    def __str__(self):
        return str(self._kwargs)

    def __repr__(self):
        return str(self)


class BaseRegistry:

    def __init__(self):
        self._resources = []
        self._loaders = []

    @property
    def count(self) -> int:
        return len(self._resources)

    def load(self, meta: ResourceDescription) -> Any:
        """
        Loads a resource or return existing one

        :param meta: The resource description
        """
        self._check_meta(meta)
        self.resolve_loader(meta)
        return meta.loader_cls(meta).load()

    def add(self, meta):
        """
        Add a resource to this pool.
        The resource is loaded and returned when ``load_pool()`` is called.

        :param meta: The resource description
        """
        self._check_meta(meta)
        self.resolve_loader(meta)
        self._resources.append(meta)

    def load_pool(self):
        """
        Loads all the data files using the configured finders.
        """
        for meta in self._resources:
            resource = self.load(meta)
            yield meta, resource

        self._resources = []

    def resolve_loader(self, meta: ResourceDescription):
        """
        Attempts to assign a loader class to a resource description

        :param meta: The resource description instance
        """
        meta.loader_cls = self.get_loader(meta, raise_on_error=True)

    def get_loader(self, meta: ResourceDescription, raise_on_error=False) -> BaseLoader:
        """
        Attempts to get a loader

        :param meta: The resource description instance
        :param raise_on_error: Raise ImproperlyConfigured if the loader cannot be resolved
        :returns: The requested loader class
        """
        for loader in self._loaders:
            if loader.name == meta.loader:
                return loader

        if raise_on_error:
            raise ImproperlyConfigured(
                "Resource has invalid loader '{}': {}\nAvailiable loaders: {}".format(
                    meta.loader, meta, [loader.name for loader in self._loaders]))

    def _check_meta(self, meta):
        if inspect.isclass(type(meta)):
            if issubclass(meta.__class__, ResourceDescription):
                return

        raise ValueError("Resource loader got type {}, not a resource description".format(type(meta)))
