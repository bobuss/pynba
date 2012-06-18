# -*- coding: utf-8 -*-
"""
    IsCool-e Pynba
    ~~~~~~~~~~~~~~

    :copyright: (c) 2012 by IsCool Entertainment.
    :license: MIT, see LICENSE for more details.
"""

import resource
from .globals import _CTX_STACK
from .collector import DataCollector

class RequestContext(object):
    """
    A new instance will be created every new request.

    :param reporter: a :class:`Reporter` instance
    :param environ: the current WSGI environ mapping
    :param config: may have these keys:
                   ``prefix`` will prepend scriptname
    """

    def __init__(self, reporter, environ, **config):
        self.reporter = reporter

        #: config['prefix'] prepends the sent scriptname to pinba.
        self.config = config

        #: futur :class:`DataCollector`
        self.pynba = None
        #: will keep a snap of :func:`resource.getrusage`
        self.resources = None
        self._scriptname = environ.get('PATH_INFO', '')
        self.hostname = environ.get('SERVER_NAME', None)
        self.servername = environ.get('HTTP_HOST', None)

    @property
    def scriptname(self):
        if self.pynba:
            return self.config.get(
                'prefix', '') + self.pynba.scriptname
        else:
            return self.config.get(
                'prefix', '') + self._scriptname

    def push(self):
        """Pushes current context into local stack.
        """
        top = _CTX_STACK.top
        if top is not self:
            _CTX_STACK.push(self)

        self.pynba = DataCollector(self._scriptname, self.hostname)
        self.pynba.start()
        self.resources = resource.getrusage(resource.RUSAGE_SELF)

    def pop(self):
        """Pops current context from local stack.
        """
        top = _CTX_STACK.top
        if top is self:
            _CTX_STACK.pop()
        self.pynba = None
        self.resources = None

    def __enter__(self):
        """Opens current scope.
        """
        self.push()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Closes current scope.
        """
        self.flush()
        self.pop()

    def flush(self):
        """Flushes timers.

        Similar to the PHP ``pinba_flush()`` function.
        scriptname sent to pinba will be prepend by config['prefix']
        """
        if not self.pynba or not self.pynba.enabled:
            return

        self.pynba.stop()
        timers = [timer for timer in self.pynba.timers if timer.elapsed]
        document_size = self.pynba.document_size
        memory_peak = self.pynba.memory_peak
        usage = resource.getrusage(resource.RUSAGE_SELF)
        ru_utime = usage.ru_utime - self.resources.ru_utime
        ru_stime = usage.ru_stime - self.resources.ru_stime

        self.reporter(
            servername= self.servername,
            hostname= self.pynba.hostname,
            scriptname= self.scriptname,
            elapsed= self.pynba.elapsed,
            timers= timers,
            ru_utime= ru_utime,
            ru_stime= ru_stime,
            document_size= document_size,
            memory_peak= memory_peak
        )

        self.pynba.flush()
