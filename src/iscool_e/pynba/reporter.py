# -*- coding: utf-8 -*-
"""
    IsCool-e Pynba
    ~~~~~~~~~~~~~~

    DOC DOC.

    :copyright: (c) 2012 by IsCool Entertainment.
    :license: BSD, see LICENSE for more details.
"""

from socket import socket, AF_INET, SOCK_DGRAM
import logging
from .pinba_pb2 import Request

class Reporter(object):
    __slots__ = ('address', 'sock')

    def __init__(self, address):
        self.address = address
        self.sock = socket(AF_INET, SOCK_DGRAM)

    def __call__(self, servername, hostname, scriptname, elapsed, timers, ru_utime=None, ru_stime=None):
        msg = Reporter.prepare(servername, hostname, scriptname, elapsed, timers, ru_utime, ru_stime)
        self.send(msg)

    @staticmethod
    def prepare(servername, hostname, scriptname, elapsed, timers, ru_utime=None, ru_stime=None):
        """pinba_flush()
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
        msg.document_size = 0
        msg.memory_peak = 0
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
                for name, values in timer.tags.iteritems():
                    if name not in dictionary:
                        dictionary.append(name)
                    if not isinstance(values, (list, tuple, set)):
                        values = [values]
                    else:
                        values = set(values)

                    for value in values:
                        value = str(value)
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
        return self.sock.sendto(msg, self.address)