import os
import shutil
from argparse import ArgumentTypeError
from demosys.core.management.base import CreateCommand


class Command(CreateCommand):
    help = "Create an effect"

    def add_arguments(self, parser):
        parser.add_argument("name", help="Name of the effect")
        parser.add_argument("--template", type=available_templates, default="cube_simple",
                            help="The effect template to clone from")

    def handle(self, *args, **options):
        name = os.path.basename(options['name'])
        path = os.path.dirname(options['name'])
        template = options['template']

        # Does the name have a path prefix?
        if path and not os.path.exists(path):
            raise ValueError("{} directory does not exist".format(path))

        # Check for python module collision
        self.try_import(name)

        # Is the name a valid identifier?
        self.validate_name(name)

        # Make sure we don't mess with existing directories
        if os.path.exists(os.path.join(path, name)):
            raise ValueError("Directory {} already exist. Aborting.".format(name))

        copy_effect_template(template, name, path)


def copy_effect_template(template_name, effect_name, dest_path):
    dest_full_path = os.path.join(dest_path, effect_name)

    # Recursive copy
    shutil.copytree(os.path.join(template_dir(), template_name), dest_full_path)

    # Rename local resource directories if present
    files = os.listdir(dest_full_path)
    for resource_dir in files:
        # Skip non-dirs
        if not os.path.isdir(os.path.join(dest_full_path, resource_dir)):
            continue

        # Rename local resource dirs to the new effect name
        local_dir = os.path.join(dest_full_path, resource_dir, template_name)
        if os.path.exists(local_dir):
            os.rename(
                local_dir,
                os.path.join(dest_full_path, resource_dir, effect_name)
            )


def available_templates(value):
    """Scan for available templates in effect_templates"""
    templates = list_templates()

    if value not in templates:
        raise ArgumentTypeError("Effect template '{}' does not exist.\n Available templates: {} ".format(
            value, ", ".join(templates)))

    return value


def list_templates():
    return os.listdir(template_dir())


def root_path():
    """Get the absolute path to the root of the demosys package"""
    module_dir = os.path.dirname(globals()['__file__'])
    return os.path.dirname(os.path.dirname(os.path.dirname(module_dir)))


def template_dir():
    """Get the absolute path to the template directory"""
    return os.path.join(root_path(), 'effect_templates')
