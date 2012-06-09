from wsgiref.simple_server import make_server
from iscool_e.pynba.middleware import PynbaMiddleware
from iscool_e.pynba.globals import pynba
from time import sleep
import logging

def simple_app(environ, start_response):
    if environ.get('PATH_INFO', None) == '/favicon.ico':
        pynba.enabled = False

    logging.debug('enter simple app')

    # TODO: implement a flush

    logging.debug('init first timer without starting it')
    timer1 = pynba.timer(foo=['foo', 'foo2'], bar=['bar', 'bar2'], baz='baz')

    logging.debug('init 2nd timer with multivalues tag')
    timer2 = pynba.timer(multi_bar=['multi1', 'multi2'], baz='baz').start()

    status = '200 OK'
    headers = [('Content-type', 'text/plain')]
    logging.debug('init 3rd as a context')
    with pynba.timer(context_bar='bar', context_baz='baz'):
        sleep(1)

    logging.debug('init 4th as a decorator')
    @pynba.timer(decorator_bar='bar', decorator_baz='baz')
    def trololo():
        return "foo"

    logging.debug('call decorated 5 times')
    trololo()
    trololo()
    trololo()
    trololo()
    trololo()

    start_response(status, headers)

    ret = ["%s: %s\n" % (key, value)
           for key, value in environ.iteritems()]
    return ret


def call_as_wsgi(callable, environ=None, close=True):
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


if __name__ == '__main__':
    app = PynbaMiddleware(simple_app, ('127.0.0.1', 30002))
    httpd = make_server('', 5000, app)
    print "Serving on port 5000..."
    httpd.serve_forever()
