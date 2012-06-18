# -*- coding: utf-8 -*-
"""
    IsCool-e Pynba
    ~~~~~~~~~~~~~~

    :copyright: (c) 2012 by IsCool Entertainment.
    :license: MIT, see LICENSE for more details.
"""

from socket import socket, AF_INET, SOCK_DGRAM
import collections
import logging
import types
from .pinba_pb2 import Request

class Reporter(object):
    """Formats and send report to pinba server.

    :param address: the address to the udp server.
    """

    __slots__ = ('address', 'sock')

    def __init__(self, address):
        self.address = address
        self.sock = socket(AF_INET, SOCK_DGRAM)

    def __call__(self, servername, hostname, scriptname, elapsed, timers,
                 ru_utime=None, ru_stime=None, document_size=None,
                 memory_peak=None):
        """
        Same as PHP pinba_flush()
        """
        msg = Reporter.prepare(servername, hostname, scriptname, elapsed,
                               timers, ru_utime, ru_stime, document_size,
                               memory_peak)
        self.send(msg)

    @staticmethod
    def prepare(servername, hostname, scriptname, elapsed, timers,
                ru_utime=None, ru_stime=None, document_size=None,
                memory_peak=None):
        """Prepares the message
        """

        logging.debug("Preprare protobuff", extra={
            'servername': servername,
            'hostname': hostname,
            'scriptname': scriptname,
            'elapsed': elapsed,
            'timers': timers
        })

        msg = Request()
        msg.hostname = hostname
        msg.server_name = servername
        msg.script_name = scriptname
        msg.request_count = 1
        msg.document_size = document_size if document_size else 0
        msg.memory_peak = memory_peak if memory_peak else 0
        msg.request_time = elapsed
        msg.ru_utime = ru_utime if ru_utime else 0.0
        msg.ru_stime = ru_stime if ru_stime else 0.0
        msg.status = 200

        if timers:
            dictionary = [] # contains mapping of tags name or value => uniq id

            for timer in timers:
                # Add a single timer
                msg.timer_hit_count.append(1)
                msg.timer_value.append(timer.elapsed)

                # Encode associated tags
                tag_count = 0
                for name, value in flattener(timer.tags):
                    if name not in dictionary:
                        dictionary.append(name)
                    if value not in dictionary:
                        dictionary.append(value)
                    msg.timer_tag_name.append(dictionary.index(name))
                    msg.timer_tag_value.append(dictionary.index(value))
                    tag_count += 1

                # Number of tags
                msg.timer_tag_count.append(tag_count)

            # Global tags dictionary
            msg.dictionary.extend(dictionary)

        # Send message to Pinba server
        return msg.SerializeToString()

    def send(self, msg):
        """Sends message to pinba server"""
        return self.sock.sendto(msg, self.address)


def flattener(tags):
    """
    Flatten tags Mapping into a list of tuple.
    :tags: must be a Mapping that implements iteritems()

    >>> flattener({'foo': 'bar'})
    [('foo', 'bar')]
    >>> flattener({'foo': 12})
    [('foo', '12')]
    >>> flattener({'foo': [12, 13]})
    [('foo', '12'), ('foo', '13')]
    >>> flattener({'foo': [12]})
    [('foo', '12')]
    >>> flattener({'foo': [12]})
    [('foo', '12')]
    >>> flattener({'foo': {'foo': [12]}})
    [('foo.foo', '12')]
    >>> flattener({'foo': lambda : ['bar', 'baz']})
    [('foo', 'bar'), ('foo', 'baz')]
    >>> flattener({'foo': {42: [12]}})
    [('foo.42', '12')]

    """
    def flatten(tags, namespace=None):
        """Flatten recursively"""
        pref = ''
        if namespace is not None:
            pref = "{0!s}.".format(namespace)

        output = []
        for key, value in tags.iteritems():
            if isinstance(value, collections.Callable):
                value = value()

            if isinstance(value, collections.Sequence) \
                and not isinstance(value, types.StringTypes):
                output.extend((pref + str(key), v) for v in set(value))
            elif isinstance(value, collections.Mapping):
                output.extend(flatten(value, namespace=key))
            else:
                output.append((pref + key, value))

        return output

    data = set(flatten(tags))
    return [(key, str(value)) for key, value in data]

