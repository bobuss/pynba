# -*- coding: utf-8 -*-
"""
    IsCool-e Pynba
    ~~~~~~~~~~~~~~

    DOC DOC.

    :copyright: (c) 2012 by IsCool Entertainment.
    :license: BSD, see LICENSE for more details.
"""

from functools import partial, wraps
from werkzeug.local import LocalStack, LocalProxy

def _lookup_object(name, fallback=False):
    top = _request_ctx_stack.top
    if top is None:
        if fallback:
            return Fallback
        raise RuntimeError('working outside of request context')
    return getattr(top, name)

_request_ctx_stack = LocalStack()
pynba = LocalProxy(partial(_lookup_object, 'pynba', True))


class Fallback(object):
    """Used to define timers globally.
    """
    class Timer(object):
        def __init__(self, **tags):
            self.tags = tags

        def __call__(self, func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                with pynba.timer(**self.tags):
                    response = func(*args, **kwargs)
                return response
            return wrapper

    @staticmethod
    def timer(**tags):
        return Fallback.Timer(**tags)
