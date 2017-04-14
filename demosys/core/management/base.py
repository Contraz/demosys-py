import argparse
from importlib import import_module


class CommandError(Exception):
    pass


class BaseCommand:
    help = ''

    def __init__(self):
        """should take cmd config"""
        pass

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        raise NotImplementedError

    def run_from_argv(self, argv):
        parser = self.create_parser(argv[0], argv[1])
        options = parser.parse_args(argv[2:])
        cmd_options = vars(options)
        args = cmd_options.pop('args', ())
        self.handle(*args, **cmd_options)

    def print_help(self, prog_name, subcommand):
        parser = self.create_parser(prog_name, subcommand)
        parser.print_help()

    def create_parser(self, prog_name, subcommand):
        """
        Create argument parser and deal with ``add_arguments``.
        :param prog_name: Name of the command (argv[0])
        :return: ArgumentParser
        """
        parser = argparse.ArgumentParser(prog_name, subcommand)
        # Add generic arguments here
        self.add_arguments(parser)
        return parser


class CreateCommand(BaseCommand):
    """Used for createproject and createeffect"""

    def validate_name(self, name):
        """Can the name be used as a python module or package?"""
        if not name:
            raise ValueError("Name cannot be empty")

        # Can the name be used as an identifier in python (module or package name)
        if not name.isidentifier():
            raise ValueError("{} is not a valid identifier".format(name))

    def try_import(self, name):
        """Attemt to import the name"""
        try:
            import_module(name)
        except ImportError:
            pass
        else:
            raise ValueError("{} conflicts with an existing python module".format(name))
