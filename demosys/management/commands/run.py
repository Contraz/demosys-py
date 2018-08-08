import demosys
from demosys.management.base import RunCommand


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
