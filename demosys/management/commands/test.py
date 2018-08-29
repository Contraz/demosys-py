import os
import sys
import pytest

import demosys
from demosys.management.base import RunCommand


class Command(RunCommand):
    help = "Run tests"

    def add_arguments(self, parser):
        parser.add_argument("module", nargs='?', default=None, type=str, help="the module to test")
        parser.add_argument("--nocontext", default=False, action="store_true")

    def handle(self, *args, **options):
        os.environ['DEMOSYS_SETTINGS_MODULE'] = 'tests.settings'
        demosys.setup()

        if not options['nocontext']:

            window = self.create_window()
            project = self.create_project()
            timeline = self.create_timeline(project)

            demosys.init(window=window, project=project, timeline=timeline)

        # Reset arguments to not confuse pytest
        sys.argv = [sys.argv[0]]
        if options.get('module'):
            sys.argv.append(options.get('module'))

        exit_code = pytest.main()
        sys.exit(exit_code)
