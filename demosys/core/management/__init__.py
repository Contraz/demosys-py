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


def load_command_class(name):
    return import_module('demosys.core.management.commands.{}'.format(name))


def execute_from_command_line(argv=None):
    if not argv:
        argv = sys.argv
    commands = find_commands(local_command_dir())
    command = argv[1] if len(argv) > 1 else None

    source = os.path.basename(argv[0])
    if source == "demosys-admin":
        print("Running as demosys-admin")

    if command in commands:
        module = load_command_class(command)
        if hasattr(module, 'run'):
            module.run(argv[2:])
        else:
            print("Command {} is not runnable".format(command))
    else:
        print("Available commands:")
        print("\n".join(commands))
