"""
Run a specific effect
"""
import demosys
from demosys.management.base import RunCommand


class Command(RunCommand):
    help = "Runs an effect"

    def add_arguments(self, parser):
        parser.add_argument("name", help="Name of the effect")

    def handle(self, *args, **options):
        demosys.setup(
            EFFECTS=[options['name']],
            PROJECT='demosys.project.default.Project',
            TIMELINE='demosys.timeline.single.Timeline'
        )

        window = self.create_window()
        project = self.create_project()
        timeline = self.create_timeline(project)

        demosys.init(window=window, project=project, timeline=timeline)
        demosys.run(window=window, project=project, timeline=timeline)
