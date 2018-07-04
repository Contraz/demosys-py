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

import moderngl


class TestCase(unittest.TestCase):

    def validate(self, filename, classname, ignore):
        root = os.path.dirname(os.path.dirname(__file__))
        with open(os.path.normpath(os.path.join(root, 'docs', 'reference', filename))) as f:
            docs = f.read()
        methods = re.findall(r'^\.\. automethod:: ([^\(\n]+)([^\n]+)', docs, flags=re.M)
        attributes = re.findall(r'^\.\. autoattribute:: ([^\n]+)', docs, flags=re.M)
        documented = set(filter(lambda x: x.startswith(classname), [a for a, b in methods] + attributes))
        implemented = set(classname + '.' + x for x in dir(getattr(moderngl, classname)) if not x.startswith('_'))
        ignored = set(classname + '.' + x for x in ignore)
        self.assertSetEqual(implemented - documented - ignored, set(), msg='Implemented but not Documented')
        self.assertSetEqual(documented - implemented, set(), msg='Documented but not Implemented')

        for method, docsig in methods:
            classname, methodname = method.split('.')
            sig = str(inspect.signature(getattr(getattr(moderngl, classname), methodname)))
            sig = sig.replace('self, ', '').replace('moderngl.', '').replace('typing.', '').replace(' -> None', '')
            sig = sig.replace('(self)', '()').replace(', *,', ',').replace('(*, ', '(')
            sig = re.sub(r'-> \'(\w+)\'', r'-> \1', sig)
            self.assertEqual(docsig, sig, msg=filename + '::' + method)

    def test_context_docs(self):
        self.validate('effect.rst', 'Effect', ['test', 'test2'])


if __name__ == '__main__':
    unittest.main()
