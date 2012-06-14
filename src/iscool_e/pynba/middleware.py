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
    default_ctx = RequestContext

    def __init__(self, app, address, **config):
        self.app = app
        self.reporter = Reporter(address)
        self.config = config

    def __call__(self, environ, start_response):
        with self.request_context(environ):
            return self.app(environ, start_response)

    def request_context(self, environ):
        return self.default_ctx(self.reporter, environ, **self.config)

