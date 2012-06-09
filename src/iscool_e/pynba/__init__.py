# -*- coding: utf-8 -*-
"""
    IsCool-e Pynba
    ~~~~~~~~~~~~~~

    DOC DOC.

    :copyright: (c) 2012 by IsCool Entertainment.
    :license: BSD, see LICENSE for more details.
"""

__version__ = '0.1'
__all__ = ['monitor', 'pynba']

from .middleware import PynbaMiddleware
from .globals import pynba

def monitor(address):
    def wrapper(func):
        return PynbaMiddleware(func, address)
    return wrapper

