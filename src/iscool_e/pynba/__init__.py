# -*- coding: utf-8 -*-
"""
    IsCool-e Pynba
    ~~~~~~~~~~~~~~

    :copyright: (c) 2012 by IsCool Entertainment.
    :license: MIT, see LICENSE for more details.
"""

__version__ = '0.1'
__all__ = ['monitor', 'pynba', 'PynbaMiddleware']

from .middleware import PynbaMiddleware
from .globals import pynba

def monitor(address, **config):
    """Simple decorator for WSGI app.
    """
    def wrapper(func):
        return PynbaMiddleware(func, address, **config)
    return wrapper

