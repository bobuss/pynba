# -*- coding: utf-8 -*-
"""
    IsCool-e Pynba
    ~~~~~~~~~~~~~~

    :copyright: (c) 2012 by IsCool Entertainment.
    :license: MIT, see LICENSE for more details.
"""

from timeit import default_timer
import functools
from copy import copy
import logging

class Timer(object):
    """
    Differences with the PHP version

    =========================== =========================
    PHP                         Python
    =========================== =========================
    pinba_timer_data_merge()    not applicabled use instance.data
    pinba_timer_data_replace()  not applicabled use instance.data
    pinba_timer_get_info()      not implemented
    =========================== =========================

    """

    __slots__ = ('tags', 'data', '_start', 'elapsed', 'parent')

    def __init__(self, tags, parent=None):
        """
        Tags values can be any scalar, mapping, sequence or callable.
        In case of a callable, redered value must be a sequence.

        :param tags: each values can be any scalar, mapping, sequence or
                     callable. In case of a callable, rendered value must
                     be a sequence.
        """
        self.tags = dict(tags)
        self.parent = parent
        self.data = None

        # timer
        self.elapsed = None
        self._start = None


    @property
    def started(self):
        """Tell if timer is started"""
        return bool(self._start)

    def delete(self):
        """Discards timer from parent
        """
        if self.parent:
            self.parent.timers.discard(self)

    def clone(self):
        """Clones timer
        """
        instance = copy(self)
        instance._start = None
        instance.elapsed = None

        if self.parent:
            self.parent.timers.add(instance)
        return instance

    def start(self):
        """Starts timer"""
        if self.started:
            raise RuntimeError('Already started')
        self._start = default_timer()
        return self

    def stop(self):
        """Stops timer"""
        if not self.started:
            raise RuntimeError('Not started')
        self.elapsed = default_timer() - self._start
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
        Example::

            @pynba.timer(foo=bar)
            def function_to_be_timed(self):
                pass
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
    This is the main data container.

    :param scriptname: the current scriptname
    :param hostname: the current hostname

    Differences with the PHP version

    =========================== =========================
    PHP                         Python
    =========================== =========================
    pinba_get_info()            not applicabled while the current
                                instance data are already exposed.
    pinba_script_name_set()     self.scriptname
    pinba_hostname_set()        not implemented, use hostname
    pinba_timers_stop()         self.stop()
    pinba_timer_start()         self.timer
    =========================== =========================

    """
    __slots__ = ('enabled', 'timers', 'scriptname', 'hostname',
                 '_start', 'elapsed')

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
        self._start = default_timer()

    def stop(self):
        """Stops current elapsed time and every attached timers.
        """
        if not self._start:
            raise RuntimeError('Not started')
        self.elapsed = default_timer() - self._start
        self._start = None
        for timer in self.timers:
            if timer.started:
                timer.stop()

    def timer(self, **tags):
        """Factory new timer.
        """
        timer = Timer(tags, self)
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
        self._start = default_timer()
        self.timers.clear()

