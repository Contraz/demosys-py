import moderngl
from demosys.conf import settings
from demosys.test.testcase import DemosysTestCase


class WindowTestCase(DemosysTestCase):

    def test_ctx(self):
        assert isinstance(self.window.ctx, moderngl.Context)

    def test_size(self):
        assert self.window.width == settings.WINDOW['size'][0]
        assert self.window.height == settings.WINDOW['size'][1]
