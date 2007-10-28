# -*- coding: utf-8 -*-
"""
    Colubrid and Dynamic Responses
"""
from colubrid import BaseApplication, Request, HttpResponse
from time import sleep


class DynamicResponse(BaseApplication):

    def __init__(self, environ, start_response):
        super(DynamicResponse, self).__init__(environ, start_response)
        self.request = Request(environ)

    def process_request(self):
        def countdown():
            yield '<h1>Dynamic Response</h1>'
            for i in xrange(500, 0, -1):
                yield ' %d ' % i
                sleep(0.01)
        self.request.send_response(countdown())


app = DynamicResponse

if __name__ == '__main__':
    from colubrid import execute
    execute()
