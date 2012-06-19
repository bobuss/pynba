IsCool Entertainment Pynba
==========================

Pynba is a WSGI Middleware for Pinba_. It allows realtime monitoring/statistics
server using MySQL as a read-only interface.

It accumulates and processes data sent over UDP by multiple PHP processes and
displays statistics in a nice human-readable form of simple "reports", also
providing read-only interface to the raw data in order to make possible
generation of more sophisticated reports and stats.

Users also can measure particular parts of the code using timers with arbitrary
tags.


Why another statistics manager ?
--------------------------------

Because Pinba rocks!

At `IsCool Entertainment`_, we already use Pinba for monitoring our PHP based
applications.


Requirements
------------

This library relies on Pinba_, Protobuf_ and Werkzeug_.
You will need to install theses packages before using Pynba.

The installation process requires setuptools to be installed.
If it is not, please refer to the installation of this package.

Setup
-----

::

    $ git clone https://github.com/IsCoolEntertainment/pynba.git
    $ python setup.py install

Usage
-----

Says that your main WSGI application is::

    def app(environ, start_response):
        ...


Import the pynba decorator, and decorate your main app with it::

    from iscool_e.pynba import monitor

    @monitor(('127.0.0.1', 30002))
    def app(environ, start_response):
        ...

Each time the app will be processed, a new UPD stream will be sent.

Eventualy, you can use timers to measure particular parts of your code.
For it, just import the pynba proxy, and use it to create new timers::

    from iscool_e.pynba import pynba

    timer = pynba.timer(foo="bar")
    timer.start()
    ...
    timer.stop()


Some use cases are available on src/examples/

Differences with PHP extension
------------------------------

About the data sent:

*   ``ru_utime`` and ``ru_stime`` represent the resource usage for the current
    process, not the shared resources.
*   ``document_size`` cannot be automaticaly processed with the current WSGI
    specification. You are able to set manually this value like this::

        pynba.document_size = [YOUR VALUE]

*   ``memory_peak`` also is currently not implemented. Like the previous data,
    you can set manually this value like this::

        pynba.memory_peak = [YOUR VALUE]

About timers:

*   The Python version permites multiple values for each timer tags.
    Just declare any sequences, mapping or callable. This example::

        pynba.timer(foo='bar', baz=['seq1', 'seq2'], qux={'map1': 'val1'})

    Will populates 4 values for 3 tags in the Pinba database::

        ('foo', 'bar'),
        ('baz, 'seq1'),
        ('baz, 'seq2'),
        ('qux.map1', 'val1')

License
-------

This package is release under the MIT Licence.
Please see LICENSE document for a full description.


Credits
-------

- Pinba_
- Werkzeug_
- Protobuf_

.. _Pinba: http://pinba.org
.. _Werkzeug: http://werkzeug.pocoo.org
.. _Protobuf: http://code.google.com/p/protobuf/
.. _`IsCool Entertainment`: http://www.iscoolentertainment.com/en/
