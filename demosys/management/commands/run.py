import demosys
from demosys.management.base import RunCommand
from demosys.exceptions import ImproperlyConfigured
from demosys.utils.module_loading import import_string
from demosys.conf import settings


class Command(RunCommand):
    help = "Run using the configured effect manager"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        demosys.setup()
        window = self.create_window()
        project = self.create_project()
        timeline = self.create_timeline(project)

        demosys.run(window=window, project=project, timeline=timeline)
