# -*- coding: utf-8 -*-
"""
    Colubrid says Hello World
"""
from colubrid import BaseApplication, Request


class HelloWorld(BaseApplication):

    def __init__(self, environ, start_response):
        super(HelloWorld, self).__init__(environ, start_response)
        self.request = Request(environ)

    def process_request(self):
        self.request.send_response('Hello World')

app = HelloWorld

if __name__ == '__main__':
    from colubrid import execute
    execute()
