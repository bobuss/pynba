# -*- coding: utf-8 -*-
"""
    IsCool-e Pynba
    ~~~~~~~~~~~~~~

    :copyright: (c) 2012 by IsCool Entertainment.
    :license: MIT, see LICENSE for more details.
"""

from functools import partial, wraps
from werkzeug.local import LocalStack, LocalProxy

def _lookup_object(name, fallback=False):
    top = _CTX_STACK.top
    if top is None:
        if fallback:
            return Fallback
        raise RuntimeError('working outside of request context')
    return getattr(top, name)

_CTX_STACK = LocalStack()
pynba = LocalProxy(partial(_lookup_object, 'pynba', True))


class Fallback(object):
    """Used to define timers globally of a context.
    """

    @staticmethod
    def timer(**tags):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                _pynba = _lookup_object("pynba", fallback=False)
                with _pynba.timer(**tags):
                    response = func(*args, **kwargs)
                return response
            return wrapper
        return decorator

