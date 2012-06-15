# -*- coding: utf-8 -*-
"""
    IsCool-e Pynba
    ~~~~~~~~~~~~~~

    :copyright: (c) 2012 by IsCool Entertainment.
    :license: MIT, see LICENSE for more details.
"""

import resource
from .globals import _request_ctx_stack
from .collector import DataCollector

class RequestContext(object):
    def __init__(self, reporter, environ, **config):
        """
        :config: may have these keys:
        ``prefix`` will prepend scriptname
        """

        self.reporter = reporter
        #: gonna be DataCollector
        self.pynba = None

        #: may use config['prefix']
        self.scriptname = config.get(
            'prefix', '') + environ.get('PATH_INFO', '')
        self.hostname = environ.get('SERVER_NAME', None)
        self.servername = environ.get('HTTP_HOST', None)

    def push(self):
        """Pushes current request into local stack.
        """
        top = _request_ctx_stack.top
        if top is not self:
            _request_ctx_stack.push(self)

        self.pynba = DataCollector(self.scriptname, self.hostname)
        self.pynba.start()
        self.resources = resource.getrusage(resource.RUSAGE_SELF)

    def pop(self):
        """Pops current request from local stack.
        """
        top = _request_ctx_stack.top
        if top is self:
            _request_ctx_stack.pop()
        self.pynba = None
        self.resources = None

    def __enter__(self):
        """Starts current scope.
        """
        self.push()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Ends current scope.
        """
        self.flush()
        self.pop()

    def flush(self):
        """Flushes timers.
        Same as PHP:pinba_flush()
        """
        if not self.pynba or not self.pynba.enabled:
            return

        self.pynba.stop()
        timers = [timer for timer in self.pynba.timers if timer.elapsed]

        usage = resource.getrusage(resource.RUSAGE_SELF)
        ru_utime = usage.ru_utime - self.resources.ru_utime
        ru_stime = usage.ru_stime - self.resources.ru_stime

        self.reporter(
            servername= self.servername,
            hostname= self.pynba.hostname,
            scriptname= self.pynba.scriptname,
            elapsed= self.pynba.elapsed,
            timers= timers,
            ru_utime= ru_utime,
            ru_stime= ru_stime
        )

        self.pynba.flush()
