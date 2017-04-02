import os
from demosys.core.management.base import CreateCommand


class Command(CreateCommand):
    help = "Create an effect"

    def add_arguments(self, parser):
        parser.add_argument("name", help="Name of the effect")

    def handle(self, *args, **options):
        name = options['name']

        # Check for python module collision
        self.try_import(name)

        # Is the name a valid identifier?
        self.validate_name(name)

        # Make sure we don't mess with existing directories
        if os.path.exists(name):
            print(f"Directory {name} already exist. Aborting.")
            return
