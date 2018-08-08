"""
Run a specific effect
"""
import demosys
from demosys.management.base import RunCommand
from demosys.project.default import Project
from demosys.timeline.single import Timeline


class Command(RunCommand):
    help = "Runs an effect"

    def add_arguments(self, parser):
        parser.add_argument("name", help="Name of the effect")

    def handle(self, *args, **options):
        demosys.setup(EFFECTS=[options['name']])
        window = self.create_window()
        project = Project(effect_module=options['name'])
        timeline = Timeline(project)

        demosys.run(window=window, project=project, timeline=timeline)
