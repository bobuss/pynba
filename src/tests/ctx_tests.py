try:
    import unittest2 as unittest
except ImportError:
    import unittest

from iscool_e.pynba.ctx import RequestContext
from iscool_e.pynba.collector import DataCollector
from iscool_e.pynba.globals import _CTX_STACK, pynba

class ContextTestCase(unittest.TestCase):
    def test_config(self):
        reporter = lambda x: x
        environ = {}
        ctx = RequestContext(reporter, environ)
        assert ctx.scriptname == ''

        ctx = RequestContext(reporter, environ, prefix="foo")
        assert ctx.scriptname.startswith('foo')

    def test_context(self):
        reporter = lambda x: x
        environ = {}

        top = _CTX_STACK.top
        ctx = RequestContext(reporter, environ)
        self.assertIsNot(ctx, top)
        ctx.push()
        top = _CTX_STACK.top
        self.assertIs(ctx, top)

        ctx.pop()
        top = _CTX_STACK.top
        self.assertIsNot(ctx, top)

    def test_context2(self):
        with self.assertRaises((RuntimeError, AttributeError)):
            pynba.enabled

        reporter = lambda *x, **y: x
        environ = {}
        with RequestContext(reporter, environ) as ctx:
            timer = pynba.timer(foo='bar')
            self.assertIn(timer, pynba.timers)

        ctx.flush()
        with self.assertRaises((RuntimeError, AttributeError)):
            self.assertIn(timer, pynba.timers)

        with ctx:
            ctx.flush()
