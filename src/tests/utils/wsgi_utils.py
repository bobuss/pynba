import wsgiref.util
# from wsgiref.util import setup_testing_defaults
from wsgiref.simple_server import make_server
from iscool_e.pynba.middleware import PynbaMiddleware
from iscool_e.pynba.globals import pynba
# from nose.tools import nottest
# setup_testing_defaults = nottest(wsgiref.util.setup_testing_defaults)
setup_testing_defaults = wsgiref.util.setup_testing_defaults

print setup_testing_defaults
# A relatively simple WSGI application. It's going to print out the
# environment dictionary after being updated by setup_testing_defaults
def simple_app(environ, start_response):
    print "foo"
    setup_testing_defaults(environ)

    # test a flush
    pynba.flush()
    timer1 = pynba.timer('foo', 'bar', 'baz')
    timer2 = pynba.timer('bar', 'baz').start()
    status = '200 OK'
    headers = [('Content-type', 'text/plain')]
    with pynba.timer('bar', 'baz'):
        print "lol"

    start_response(status, headers)

    ret = ["%s: %s\n" % (key, value)
           for key, value in environ.iteritems()]
    return ret


# def call_as_wsgi(callable, environ=None, close=True):
#     """Invoke callable via WSGI, returning status, headers, response."""
#     if environ is None:
#         environ = {}
#         setup_testing_defaults(environ)
# 
#     meta = []
#     def start_response(status, headers):
#         meta.extend((status, headers))
# 
#     result = callable(environ, start_response)
#     content = ''.join(result)
#     if close and hasattr(result, 'close'):
#         result.close()
#     return meta[0], meta[1], content


if __name__ == '__main__':
    app = PynbaMiddleware(simple_app, ('127.0.0.1', 3456))
    httpd = make_server('', 5000, app)
    print "Serving on port 5000..."
    httpd.serve_forever()
