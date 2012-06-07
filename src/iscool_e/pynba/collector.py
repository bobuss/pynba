from time import clock as time
import functools
from copy import copy
import logging

class Timer(object):
    """
    pinba_timer_tags_merge
    and pinba_timer_tags_replace
    by python standard methods

    pinba_timer_data_merge
    pinba_timer_data_replace not implemented, use instance.data

    pinba_timer_get_info() not implemented
    """

    __slots__ = ('tags', 'data', '_start', 'elapsed')

    def __init__(self, **tags):
        self.tags = dict(tags)
        self.data = None

        # timer
        self.elapsed = None
        self._start = None

    @property
    def started(self):
        """Tell if timer is started"""
        return bool(self._start)

    def clone(self):
        """Clones timer"""
        instance = copy(self)
        instance._start = None
        instance.elapsed = None
        return instance

    def start(self):
        """Starts timer"""
        if self.started:
            raise RuntimeError('Already started')
        self._start = time()
        return self

    def stop(self):
        """Stops timer"""
        if not self.started:
            raise RuntimeError('Not started')
        self.elapsed = time() - self._start
        self._start = None
        return self

    def __enter__(self):
        """Acts as a context manager.
        Automatically starts timer
        """
        if not self.started:
            self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Closes context manager.
        Automatically stops timer
        """
        if self.started:
            self.stop()

    def __call__(self, func):
        """Acts as a decorator.
        Automatically starts and stops timer's clone.
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with self.clone():
                response = func(*args, **kwargs)
            return response
        return wrapper

    def __repr__(self):
        label, period = '', ''
        if self._start:
            label = ' started:'
            period = self._start
        elif self.elapsed:
            label = ' elapsed:'
            period = self.elapsed

        return '<{0}({1}){2}{3}>'.format(
            self.__class__.__name__,
            self.tags,
            label, period)


class DataCollector(object):
    """
    pinba_get_info() not implemented
    pinba_script_name_set() not implemented, use self.scriptname
    pinba_hostname_set() not implemented, use hostname
    """
    __slots__ = ('enabled', 'timers', 'scriptname', 'hostname',
                 '_start', 'elapsed')

    class Timer(Timer):
        __slots__ = (list(Timer.__slots__) + ['parent'])
        def __init__(self, tags, parent):
            Timer.__init__(self, **tags)
            self.parent = parent

        def delete(self):
            """Overwrites Timer.
            Discards timer from parent
            """
            self.parent.timers.discard(self)

        def clone(self):
            """Overwrites Timer.
            Adds timer to parent
            """
            cloned = Timer.clone(self)
            self.parent.timers.add(cloned)
            return cloned

    def __init__(self, scriptname=None, hostname=None):
        self.enabled = True
        self.timers = set()
        self.scriptname = scriptname
        self.hostname = hostname
        self._start = None
        self.elapsed = None

    @property
    def started(self):
        """Tells if is started"""
        return bool(self._start)

    def start(self):
        """Starts"""
        if self._start:
            raise RuntimeError('Already started')
        self._start = time()

    def stop(self):
        """Stops.
        Same as PHP:pinba_timers_stop()
        """
        if not self._start:
            raise RuntimeError('Not started')
        self.elapsed = time() - self._start
        self._start = None
        for timer in self.timers:
            if timer.started:
                timer.stop()

    def timer(self, **tags):
        """Factory new timer.
        Same as PHP:pinba_timer_start()
        """
        timer = self.Timer(tags, self)
        self.timers.add(timer)

        return timer

    def flush(self):
        """Flushs.
        """
        logging.debug('flush', extra={
            'timers': self.timers,
            'elapsed': self.elapsed,
        })

        self.elapsed = None
        self._start = time()
        self.timers.clear()

