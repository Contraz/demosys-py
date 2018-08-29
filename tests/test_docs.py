"""
Documentation testing

Inspired by:
https://github.com/cprogrammer1994/ModernGL/blob/master/tests/test_documentation.py
by Szabolcs Dombi

This version is simplified:
* Only test if the attribute or method is present in the class. Function parameters are not inspected.
* Include ignore pattern in the implemented set
"""
import os
import re

from demosys.test import DemosysTestCase
from demosys.utils import module_loading

os.environ['DEMOSYS_SETTINGS_MODULE'] = 'tests.settings'  # noqa


class TestCase(DemosysTestCase):
    """
    Test reference docs
    """
    def validate(self, filename, module, classname, ignore):
        """
        Finds all automethod and autoattribute statements in an rst file
        comparing them to the attributes found in the actual class
        """
        with open(os.path.normpath(os.path.join('docs', 'reference', filename))) as f:
            docs = f.read()

        module = module_loading.import_module(module)

        methods = re.findall(r'^\.\. automethod:: ([^\(\n]+)', docs, flags=re.M)
        attributes = re.findall(r'^\.\. autoattribute:: ([^\n]+)', docs, flags=re.M)

        documented = set(filter(lambda x: x.startswith(classname), [a for a in methods] + attributes))
        implemented = set(classname + '.' + x for x in dir(getattr(module, classname))
                          if not x.startswith('_') or x == '__init__')
        print(implemented)
        ignored = set(classname + '.' + x for x in ignore)

        self.assertSetEqual(implemented - documented - ignored, set(), msg='Implemented but not Documented')
        self.assertSetEqual(documented - implemented - ignored, set(), msg='Documented but not Implemented')

    def test_demosys_contex_base(self):
        self.validate('demosys.context.base.rst', 'demosys.context.base', 'BaseWindow', [])

    def test_demosys_context_glfw(self):
        self.validate('demosys.context.glfw.rst', 'demosys.context.glfw', 'Window', [])
