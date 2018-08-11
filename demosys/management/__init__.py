import os
import pkgutil
import sys
from typing import List

from demosys.utils.module_loading import import_module


def find_commands(command_dir: str) -> List[str]:
    """
    Get all command names in the a folder

    :return: List of commands names
    """
    if not command_dir:
        return []

    return [name for _, name, is_pkg in pkgutil.iter_modules([command_dir])
            if not is_pkg and not name.startswith('_')]


def system_command_dir() -> str:
    command_dir = os.path.dirname(globals()['__file__'])
    command_dir = os.path.join(command_dir, 'commands')
    return command_dir


def project_command_dir() -> str:
    module_name = project_settings_path()
    if not module_name:
        return None

    module = import_module(module_name)
    return os.path.join(os.path.dirname(module.__file__), 'management', 'commands')


def project_settings_path() -> str:
    try:
        return os.environ['DEMOSYS_SETTINGS_MODULE']
    except KeyError:
        return None


def project_package_name() -> str:
    package = project_settings_path()
    if not package:
        return None
    return package[:package.rfind(".")]


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
    system_commands = find_commands(system_command_dir())
    project_commands = find_commands(project_command_dir())

    project_package = project_package_name()

    command = argv[1] if len(argv) > 1 else None

    # Are we running a core command?
    if command in system_commands:
        cmd = load_command_class('demosys', command)
        cmd.run_from_argv(argv)
    elif command in project_commands:
        cmd = load_command_class(project_package, command)
        cmd.run_from_argv(argv)
    else:
        print("Available commands:")
        for name in system_commands:
            print(" - {}".format(name))
        for name in project_commands:
            print(" - {}".format(name))
