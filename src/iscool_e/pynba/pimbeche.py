from socket import socket, AF_INET, SOCK_DGRAM
import logging
from .pinba_pb2 import Request

class Pimbeche(object):
    def __init__(self, address):
        self.address = address
        self.sock = socket(AF_INET, SOCK_DGRAM)

    def __call__(self, servername, hostname, scriptname, elapsed, timers):
        msg = Pimbeche.prepare(servername, hostname, scriptname, elapsed, timers)
        self.send(msg)

    @staticmethod
    def prepare(servername, hostname, scriptname, elapsed, timers):
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
        msg.ru_utime = 0.0
        msg.ru_stime = 0.0
        msg.status = 200

        if timers:
            dictionary = [] # contains mapping of tags name or value => uniq id

            for timer in timers:
                # Add a single timer
                msg.timer_hit_count.append(1)
                msg.timer_value.append(timer.elapsed)

                # Encode associated tags
                tag_count = 0
                for name, value in timer.tags.iteritems():
                    if name not in dictionary:
                        dictionary.append(name)
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