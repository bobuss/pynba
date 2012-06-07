try:
    import unittest2 as unittest
except ImportError:
    import unittest

from wsgiref.simple_server import make_server

from nose.tools import nottest
from wsgiref.util import setup_testing_defaults
setup_testing_defaults = nottest(setup_testing_defaults)

from iscool_e.pynba.middleware import PynbaMiddleware
from iscool_e.pynba.globals import pynba

class MiddlewareTestCase(unittest.TestCase):
    def test_context(self):
        def app(environ, start_response):
            with pynba.timer(foo="bar") as timer:
                status = '200 OK'
                headers = [('Content-type', 'text/plain')]
                start_response(status, headers)

            return ['foo', 'bar']

        middleware = PynbaMiddleware(app, ('127.0.0.1', 5000))
        self.call_as_wsgi(middleware)

    def call_as_wsgi(self, callable, environ=None, close=True):
        """Invoke callable via WSGI, returning status, headers, response."""
        if environ is None:
            environ = {}
            setup_testing_defaults(environ)

        meta = []
        def start_response(status, headers):
            meta.extend((status, headers))

        result = callable(environ, start_response)
        content = ''.join(result)
        if close and hasattr(result, 'close'):
            result.close()
        return meta[0], meta[1], content
