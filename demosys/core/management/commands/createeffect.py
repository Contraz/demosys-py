import os
from demosys.core.management.base import CreateCommand


class Command(CreateCommand):
    help = "Create an effect"

    def add_arguments(self, parser):
        parser.add_argument("name", help="Name of the effect")

    def handle(self, *args, **options):
        name = os.path.basename(options['name'])
        path = os.path.dirname(options['name'])

        # Does the name have a path prefix?
        if path and not os.path.exists(path):
            raise ValueError("{} directory does not exist".format(path))

        # Check for python module collision
        self.try_import(name)

        # Is the name a valid identifier?
        self.validate_name(name)

        # Make sure we don't mess with existing directories
        if os.path.exists(name):
            print("Directory {} already exist. Aborting.".format(name))
            return

        os.mkdir(os.path.join(path, name))
        os.makedirs(os.path.join(path, name, 'textures', name))
        os.makedirs(os.path.join(path, name, 'shaders', name))

        # Create effect.py
        with open(os.path.join(path, name, 'effect.py'), 'w') as fd:
            fd.write(default_effect(name))

        # Create default.glsl
        with open(os.path.join(path, name, 'shaders', name, 'default.glsl'), 'w') as fd:
            fd.write(default_shader())


def default_effect(name):
    file_path = os.path.join(root_path(), 'effects/default/effect.py')
    with open(file_path, 'r') as fd:
        data = fd.read()

    data = data.replace('"default/default.glsl"', '"{}/default.glsl"'.format(name))
    return data


def default_shader():
    file_path = os.path.join(root_path(), 'effects/default/shaders/default/default.glsl')
    with open(file_path, 'r') as fd:
        data = fd.read()

    return data


def root_path():
    module_dir = os.path.dirname(globals()['__file__'])
    return os.path.dirname(os.path.dirname(os.path.dirname(module_dir)))
