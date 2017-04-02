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

        os.mkdir(name)
        os.mkdir(os.path.join(name, 'textures'))
        os.mkdir(os.path.join(name, 'shaders'))

        # Create effect.py
        with open(os.path.join(name, 'effect.py'), 'w') as fd:
            fd.write(default_effect())

        # Create default.glsl
        with open(os.path.join(name, 'shaders', 'default.glsl'), 'w') as fd:
            fd.write(default_shader())


def default_effect():
    file_path = os.path.join(root_path(), 'effects/default/effect.py')
    return open(file_path, 'r').read()


def default_shader():
    file_path = os.path.join(root_path(), 'effects/default/shaders/default.glsl')
    return open(file_path, 'r').read()


def root_path():
    module_dir = os.path.dirname(globals()['__file__'])
    return os.path.dirname(os.path.dirname(os.path.dirname(module_dir)))
