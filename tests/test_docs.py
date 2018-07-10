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

# Modules we want to remove from types
MODULES = [
    'demosys.',
    'opengl.',
    'texture.',
    'shader.',
    'moderngl.',
    'rocket.',
    'tracks.',
    'scene.',
]

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
            sig = sig.replace('self, ', '').replace('typing.', '').replace(' -> None', '')
            for m in MODULES:
                sig = sig.replace(m, '')
            sig = sig.replace('(self)', '()').replace(', *,', ',').replace('(*, ', '(')
            sig = re.sub(r'-> \'(\w+)\'', r'-> \1', sig)
            self.assertEqual(docsig, sig, msg=filename + '::' + method)

    def test_effect_docs(self):
        self.validate(
            os.path.join('reference', 'effect.rst'),
            effects, 'Effect', [])

    def test_texture2d_docs(self):
        self.validate(
            os.path.join('reference', 'texture2d.rst'),
            opengl, 'Texture2D', ['quad', 'shader'])

    def test_fbo_docs(self):
        self.validate(
            os.path.join('reference', 'fbo.rst'),
            opengl, 'FBO', [])

    def test_shader_docs(self):
        self.validate(
            os.path.join('reference', 'shaderprogram.rst'),
            opengl, 'ShaderProgram', []
        )

    def test_vao_docs(self):
        self.validate(
            os.path.join('reference', 'vao.rst'),
            opengl, 'VAO', []
        )

if __name__ == '__main__':
    unittest.main()
