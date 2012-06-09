try:
    import unittest2 as unittest
except ImportError:
    import unittest

from iscool_e.pynba.ctx import RequestContext
from iscool_e.pynba.collector import DataCollector
from iscool_e.pynba.globals import _request_ctx_stack, pynba

class ContextTestCase(unittest.TestCase):
    def test_context(self):
        reporter = lambda x: x
        environ = {}

        top = _request_ctx_stack.top
        ctx = RequestContext(reporter, environ)
        self.assertIsNot(ctx, top)
        ctx.push()
        top = _request_ctx_stack.top
        self.assertIs(ctx, top)

        ctx.pop()
        top = _request_ctx_stack.top
        self.assertIsNot(ctx, top)

    def test_context2(self):
        with self.assertRaises(RuntimeError):
            pynba.enabled

        reporter = lambda *x, **y: x
        environ = {}
        with RequestContext(reporter, environ) as ctx:
            timer = pynba.timer(foo='bar')
            self.assertIn(timer, pynba.timers)

        ctx.flush()
        with self.assertRaises(RuntimeError):
            self.assertIn(timer, pynba.timers)

        with ctx:
            ctx.flush()
