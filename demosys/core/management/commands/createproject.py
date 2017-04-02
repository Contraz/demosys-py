# FIXME: Rewrite this into something less horrible in the future
# Right now we just want this to work
import os
from importlib import import_module

HELP = "Create a project"


def print_usage():
    print("Usage:")
    print("  crateproject <name>")


def run(args):
    if not args:
        print_usage()
        return

    name = args[0]
    print(f"Creating project '{name}'")

    # Check for python module collision
    try:
        import_module(name)
    except ImportError:
        pass
    else:
        raise ValueError(f"{name} conflicts with an existing python module")

    # Is the name a valid identifier?
    validate_name(name)

    # Make sure we don't mess with existing directories
    if os.path.exists(name):
        print(f"Directory {name} already exist. Aborting.")
        return

    # Create the project directory
    os.makedirs(name)

    # Use the default settings file
    os.environ['DEMOSYS_SETTINGS_MODULE'] = 'demosys.conf.default_settings'
    from demosys.conf import settings
    from demosys.conf import settingsfile

    with open(os.path.join(name, 'settings.py'), 'w') as fd:
        fd.write(settingsfile.create(settings))

    manage_file = 'manage.py'
    with open(manage_file, 'w') as fd:
        fd.write(gen_manage_py(name))

    os.chmod(manage_file, 0o777)


def validate_name(name):
    if not name:
        raise ValueError("Name cannot be empty")

    # Can the name be used as an identifier in python (module or package name)
    if not name.isidentifier():
        raise ValueError(f"{name} is not a valid identifier")


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
        '    execute_from_command_line(sys.argv)'
    ]
    return "\n".join(lines)
