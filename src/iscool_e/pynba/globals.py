# -*- coding: utf-8 -*-
"""
    IsCool-e Pynba
    ~~~~~~~~~~~~~~

    DOC DOC.

    :copyright: (c) 2012 by IsCool Entertainment.
    :license: BSD, see LICENSE for more details.
"""

from functools import partial
from werkzeug.local import LocalStack, LocalProxy

def _lookup_object(name):
    top = _request_ctx_stack.top
    if top is None:
        raise RuntimeError('working outside of request context')
    return getattr(top, name)


_request_ctx_stack = LocalStack()
pynba = LocalProxy(partial(_lookup_object, 'pynba'))
