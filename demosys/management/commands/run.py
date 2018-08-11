import demosys
from demosys.management.base import RunCommand


class Command(RunCommand):
    help = "Run the project"

    def handle(self, *args, **options):
        demosys.setup()

        window = self.create_window()
        project = self.create_project()
        timeline = self.create_timeline(project)

        demosys.init(window=window, project=project, timeline=timeline)
        demosys.run(window=window, project=project, timeline=timeline)
