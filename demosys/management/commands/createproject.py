import os
import string

from demosys.management.base import CreateCommand


class Command(CreateCommand):
    help = "Create a project"

    def add_arguments(self, parser):
        parser.add_argument("name", help="Name of the project")

    def handle(self, *args, **options):
        self.project_name = options['name']
        self.template_dir = self.get_template_dir()

        if not self.initial_sanity_check():
            return

        self.create_project()

    def initial_sanity_check(self):
        """Checks if we can create the project"""
        # Check for python module collision
        self.try_import(self.project_name)

        # Is the name a valid identifier?
        self.validate_name(self.project_name)

        # Make sure we don't mess with existing directories
        if os.path.exists(self.project_name):
            print("Directory {} already exist. Aborting.".format(self.project_name))
            return False

        if os.path.exists('manage.py'):
            print("A manage.py file already exist in the current directory. Aborting.")
            return False

        return True

    def create_project(self):
        # Create the project directory
        os.makedirs(self.project_name)

        self.create_entrypoint()
        self.create_settings()
        self.create_project_file()

    def create_entrypoint(self):
        """Write manage.py in the current directory"""
        with open(os.path.join(self.template_dir, 'manage.py'), 'r') as fd:
            data = fd.read().format(project_name=self.project_name)

        with open('manage.py', 'w') as fd:
            fd.write(data)

        os.chmod('manage.py', 0o777)

    def create_settings(self):
        with open(os.path.join(self.template_dir, 'project', 'settings.py'), 'r') as fd:
            template = string.Template(fd.read())

        with open(os.path.join(self.project_name, 'settings.py'), 'w') as fd:
            fd.write(template.substitute(project_name=self.project_name))

    def get_template_dir(self):
        """Returns the absolute path to template directory"""
        directory = os.path.dirname(os.path.abspath(__file__))
        directory = os.path.dirname(os.path.dirname(directory))
        directory = os.path.join(directory, 'project_template')
        return directory

    def create_project_file(self):
        with open(os.path.join(self.template_dir, 'project', 'project.py'), 'r') as fd:
            template = string.Template(fd.read())

        with open(os.path.join(self.project_name, 'project.py'), 'w') as fd:
            fd.write(template.substitute(project_name=self.project_name))
