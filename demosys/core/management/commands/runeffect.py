"""
Run a specific effect
"""
import demosys
from demosys.core.management.base import CreateCommand
from demosys.effects.managers import SingleEffectManager


class Command(CreateCommand):
    help = "Runs an effect"

    def add_arguments(self, parser):
        parser.add_argument("name", help="Name of the effect")

    def handle(self, *args, **options):
        demosys.setup()
        manager = SingleEffectManager(effect_module=options['name'])
        demosys.run(manager=manager)
