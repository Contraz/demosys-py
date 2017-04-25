import demosys
from demosys.core.management.base import BaseCommand
from demosys.core.exceptions import ImproperlyConfigured
from demosys.utils.module_loading import import_string
from demosys.conf import settings


class Command(BaseCommand):
    help = "Run using the configured effect manager"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        demosys.setup()
        manager_path = getattr(settings, 'EFFECT_MANAGER')
        if not manager_path:
            raise ImproperlyConfigured("EFFECT_MANAGER not properly configured in settings")
        print(manager_path)
        try:
            manager_cls = import_string(manager_path)
        except ImportError as e:
            raise ImproperlyConfigured("EFFECT_MANAGER '{}' failed to initialize: {}".format(manager_path, e))

        manager = manager_cls()
        demosys.run(manager=manager)
