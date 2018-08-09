import os
import sys
import pytest

import demosys
from demosys.management.base import RunCommand


class Command(RunCommand):

    def add_arguments(self, parser):
        parser.add_argument("module", nargs='?', default=None, type=str, help="the module to test")

    def handle(self, *args, **options):
        os.environ['DEMOSYS_SETTINGS_MODULE'] = 'tests.settings'
        demosys.setup()

        window = self.create_window()
        project = self.create_project()
        timeline = self.create_timeline(project)

        demosys.init(window=window, project=project, timeline=timeline)

        # Reset arguments to not confuse pytest
        sys.argv = [sys.argv[0]]
        if options.get('module'):
            sys.argv.append(options.get('module'))

        pytest.main()
