"""
Run a specific effect
"""
import demosys
from demosys.core.management.base import CreateCommand


class Command(CreateCommand):
    help = "Runs an effect"

    def add_arguments(self, parser):
        parser.add_argument("name", help="Name of the effect")

    def handle(self, *args, **options):
        demosys.setup()
        demosys.run(runeffect=options['name'])
