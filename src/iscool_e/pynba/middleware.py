from .pimbeche import Pimbeche
from .ctx import RequestContext

class PynbaMiddleware(object):
    def __init__(self, app, address):
        self.app = app
        self.pimbeche = Pimbeche(address)

    def __call__(self, environ, start_response):
        with self.request_context(environ):
            response = self.app(environ, start_response)
        return response

    def request_context(self, environ):
        return RequestContext(self.pimbeche, environ)
