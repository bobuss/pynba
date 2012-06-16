# -*- coding: utf-8 -*-
"""
    IsCool-e Pynba
    ~~~~~~~~~~~~~~

    :copyright: (c) 2012 by IsCool Entertainment.
    :license: MIT, see LICENSE for more details.
"""

from .reporter import Reporter
from .ctx import RequestContext

class PynbaMiddleware(object):
    """Used to decorate main apps.

    :param app: The main WSGI app that will be monitored.
    :param address: The address to the UDP server.
    :param config: basically optional parameters
     """

    default_ctx = RequestContext

    def __init__(self, app, address, **config):
        self.app = app
        self.reporter = Reporter(address)
        self.config = config

    def __call__(self, environ, start_response):
        with self.request_context(environ):
            return self.app(environ, start_response)

    def request_context(self, environ):
        """
        :param environ: The WSGI environ mapping.
        :return: will return a new instance of :class:`~.ctx.RequestContext`
        """
        return self.default_ctx(self.reporter, environ, **self.config)

