import os
import sys
import pkgutil
from demosys.utils.module_loading import import_module


def find_commands(command_dir):
    """
    Get all command names in the command folder
    :return: List of commands names
    """
    return [name for _, name, is_pkg in pkgutil.iter_modules([command_dir])
            if not is_pkg and not name.startswith('_')]


def local_command_dir():
    command_dir = os.path.dirname(globals()['__file__'])
    command_dir = os.path.join(command_dir, 'commands')
    return command_dir


def load_command_class(app_name, name):
    module = import_module('{}.management.commands.{}'.format(app_name, name))
    return module.Command()


def execute_from_command_line(argv=None):
    """
    Currently the only entrypoint (manage.py, demosys-admin)
    """
    if not argv:
        argv = sys.argv

    # prog_name = argv[0]
    commands = find_commands(local_command_dir())
    command = argv[1] if len(argv) > 1 else None

    if command in commands:
        cmd = load_command_class('demosys.core', command)
        cmd.run_from_argv(argv)
    else:
        print("Available commands:")
        for c in commands:
            print(" - {}".format(c))
