IsCool Entertainment Pynba
==========================

Pynba is a WSGI Middleware for Pinba_. It allows realtime monitoring/statistics
server using MySQL as a read-only interface.

It accumulates and processes data sent over UDP by multiple PHP processes and
displays statistics in a nice human-readable form of simple "reports", also
providing read-only interface to the raw data in order to make possible
generation of more sophisticated reports and stats.

With users also can measure particular parts of the code using timers with
arbitrary tags.


Requirements
------------

This library relies on Pynba_, Protobuf_ and Werkeug_.
You will need to install theses packages before using Pynba.


Setup
-----

The installation process requires setuptools to be installed.
If it is not, please refer to the installation of this package.

Then, download this package, and execute this command

> python setup.py install

It will download and install automacaly

Usage
-----

Says that your main WSGI application is

    def app(environ, start_response):
        ...


Import the pynba decorator, and decorate your main app with it

    from iscool_e.pynba import monitor

    @monitor(('127.0.0.1', 30002))
    def app(environ, start_response):
        ...

Each time the app will be processed, a new UPD stream will be sent.

Eventualy, you can use timers to measure particular parts of your code.
For it, just import the pynba proxy, and use it to create new timers/

    from iscool_e.pynba import pynba

    timer = pynba.timer(foo="bar")
    timer.start()
    ...
    timer.stop()


Some use cases are available on src/examples/


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