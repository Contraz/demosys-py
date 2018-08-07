"""
Run a specific effect
"""
import demosys
from demosys.management.base import CreateCommand
from demosys.project.default import Project


class Command(CreateCommand):
    help = "Runs an effect"

    def add_arguments(self, parser):
        parser.add_argument("name", help="Name of the effect")

    def handle(self, *args, **options):
        demosys.setup(settings_override={'EFFECTS': [options['name']]})
        project = Project(effect_module=options['name'])
        demosys.run(project=project)
