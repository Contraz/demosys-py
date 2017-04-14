import os
from demosys.core.management.base import CreateCommand


class Command(CreateCommand):
    help = "Create a project"

    def add_arguments(self, parser):
        parser.add_argument("name", help="Name of the project")

    def handle(self, *args, **options):
        name = options['name']

        # Check for python module collision
        self.try_import(name)

        # Is the name a valid identifier?
        self.validate_name(name)

        # Make sure we don't mess with existing directories
        if os.path.exists(name):
            print("Directory {} already exist. Aborting.".format(name))
            return

        manage_file = 'manage.py'
        if os.path.exists(manage_file):
            print("A manage.py file already exist in the current directory. Aborting.")
            return

        # Create the project directory
        os.makedirs(name)

        # Use the default settings file
        os.environ['DEMOSYS_SETTINGS_MODULE'] = 'demosys.conf.default_settings'
        from demosys.conf import settings
        from demosys.conf import settingsfile

        with open(os.path.join(name, 'settings.py'), 'w') as fd:
            fd.write(settingsfile.create(settings))

        with open(manage_file, 'w') as fd:
            fd.write(gen_manage_py(name))

        os.chmod(manage_file, 0o777)


def gen_manage_py(project_name):
    lines = [
        '#!/usr/bin/env python3',
        'import os',
        'import sys',
        '',
        'if __name__ == "__main__":',
        '    os.environ.setdefault("DEMOSYS_SETTINGS_MODULE", "{}.settings")'.format(project_name),
        '',
        '    from demosys.core.management import execute_from_command_line',
        '',
        '    execute_from_command_line(sys.argv)',
        '',
    ]
    return "\n".join(lines)
