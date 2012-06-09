# -*- coding: utf-8 -*-
"""
    IsCool-e Pynba
    ~~~~~~~~~~~~~~

    DOC DOC.

    :copyright: (c) 2012 by IsCool Entertainment.
    :license: BSD, see LICENSE for more details.
"""

from .reporter import Reporter
from .ctx import RequestContext

class PynbaMiddleware(object):
    def __init__(self, app, address):
        self.app = app
        self.reporter = Reporter(address)

    def __call__(self, environ, start_response):
        with self.request_context(environ):
            return self.app(environ, start_response)

    def request_context(self, environ):
        return RequestContext(self.reporter, environ)

