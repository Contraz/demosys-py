"""
Run a specific effect
"""
import demosys
from demosys.management.base import RunCommand


class Command(RunCommand):
    help = "Runs an effect"

    def add_arguments(self, parser):
        parser.add_argument("effect_package", help="Python path to effect package or effect class")

    def handle(self, *args, **options):
        demosys.setup(
            PROJECT='demosys.project.default.Project',
            TIMELINE='demosys.timeline.single.Timeline'
        )

        window = self.create_window()
        project = self.create_project(options['effect_package'])
        timeline = self.create_timeline(project)

        demosys.init(window=window, project=project, timeline=timeline)
        demosys.run(window=window, project=project, timeline=timeline)
