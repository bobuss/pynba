from .globals import _request_ctx_stack
from .collector import DataCollector

class RequestContext(object):
    def __init__(self, pimbeche, environ):
        self.pimbeche = pimbeche
        #: gonna be DataCollector
        self.pynba = None
        self.scriptname = environ.get('PATH_INFO', None)
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

    def pop(self):
        """Pops current request from local stack.
        """
        top = _request_ctx_stack.top
        if top is self:
            _request_ctx_stack.pop()
        self.pynba = None

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

        self.pimbeche(
            servername= self.servername,
            hostname= self.pynba.hostname,
            scriptname= self.pynba.scriptname,
            elapsed= self.pynba.elapsed,
            timers= timers
        )

        self.pynba.flush()

