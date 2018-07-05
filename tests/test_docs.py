"""
Documentation testing

Based on:
https://github.com/cprogrammer1994/ModernGL/blob/master/tests/test_documentation.py
by Szabolcs Dombi
"""
import inspect
import os
import re
import unittest

os.environ['DEMOSYS_SETTINGS_MODULE'] = 'tests.settings'

import demosys
from demosys import effects
from demosys import opengl

class TestCase(unittest.TestCase):

    def validate(self, filename, module, classname, ignore):
        root = os.path.dirname(os.path.dirname(__file__))
        with open(os.path.normpath(os.path.join(root, 'docs', 'source', filename))) as f:
            docs = f.read()
        methods = re.findall(r'^\.\. automethod:: ([^\(\n]+)([^\n]+)', docs, flags=re.M)
        attributes = re.findall(r'^\.\. autoattribute:: ([^\n]+)', docs, flags=re.M)
        documented = set(filter(lambda x: x.startswith(classname), [a for a, b in methods] + attributes))
        implemented = set(classname + '.' + x for x in dir(getattr(module, classname)) if not x.startswith('_'))
        ignored = set(classname + '.' + x for x in ignore)
        self.assertSetEqual(implemented - documented - ignored, set(), msg='Implemented but not Documented')
        self.assertSetEqual(documented - implemented, set(), msg='Documented but not Implemented')

        for method, docsig in methods:
            classname, methodname = method.split('.')
            sig = str(inspect.signature(getattr(getattr(module, classname), methodname)))
            sig = sig.replace('self, ', '').replace('moderngl.', '').replace('typing.', '').replace(' -> None', '')
            sig = sig.replace('(self)', '()').replace(', *,', ',').replace('(*, ', '(')
            sig = re.sub(r'-> \'(\w+)\'', r'-> \1', sig)
            self.assertEqual(docsig, sig, msg=filename + '::' + method)

    def test_effect_docs(self):
        self.validate(os.path.join('reference', 'effect.rst'), effects, 'Effect', [])

    def test_texture2d_docs(self):
        self.validate(
            os.path.join('reference', 'texture2d.rst'),
            opengl,
            'Texture2D',
            ['quad', 'shader']
        )

if __name__ == '__main__':
    unittest.main()
