from wsgiref.simple_server import make_server
from iscool_e.pynba import PynbaMiddleware, pynba
from time import sleep

def app(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/plain')]
    start_response(status, headers)

    #: You can use a single timer
    timer = pynba.timer(tag1='foo', tag2='bar')
    timer.start()
    sleep(.1)
    timer.stop()

    #: Or benchmark an algorhythm with a context processor
    with pynba.timer(tag3='foo', tag4='bar'):
        sleep(.1)

    #: Evently benchmark a function with a decorator
    @pynba.timer(tag5='foo', tag6='bar'):
    def long_process(self):
        sleep(.1)

    long_process()


    return """
    Type
        SELECT * FROM  `request`
    on MySQL to found the current request {scriptname}.

    Type
        SELECT * FROM  `timer`
    on MySQL to found the assocated timer.
    """.format(scriptname= pynba.scriptname)


#: Monitor this app
monitored_app = PynbaMiddleware(app, ('127.0.0.1', 30002))


if __name__ == '__main__':
    httpd = make_server('', 5000, monitored_app)
    print "Serving on port 5000..."
    httpd.serve_forever()
