try:
    import unittest2 as unittest
except ImportError:
    import unittest

from iscool_e.pynba.globals import Fallback, pynba, _CTX_STACK
from contextlib import contextmanager

class GlobalTestCase(unittest.TestCase):
    def test_context(self):
        @pynba.timer(foo="bar")
        def foo():
            """docstring for foo"""
            pass

        with self.assertRaises(RuntimeError):
            foo()

        class Ctx(object):
            def __init__(self):
                class X(object):
                    @contextmanager
                    def timer(self, *args, **kwargs):
                        yield
                self.pynba = X()

        bar = Ctx()
        _CTX_STACK.push(bar)

        foo()

