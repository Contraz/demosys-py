import os

import pytest

import demosys
from demosys.management.base import RunCommand


class Command(RunCommand):

    def handle(self, *args, **options):
        os.environ['DEMOSYS_SETTINGS_MODULE'] = 'tests.settings'
        demosys.setup()

        window = self.create_window()
        project = self.create_project()
        timeline = self.create_timeline(project)

        demosys.init(window=window, project=project, timeline=timeline)

        pytest.run()
