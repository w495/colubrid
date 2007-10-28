#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    webpylike application
"""
import os
from colubrid import WebpyApplication, Request, HttpResponse


class HelloWorld(object):
    def GET(self, name):
        name = name or 'World'
        try:
            times = int(self.request.args['times'])
        except:
            times = 1
        response = HttpResponse('\n'.join(['Hello %s!' % name] * times))
        response['Content-Type'] = 'text/plain'
        return response


class WebpyLike(WebpyApplication):
    urls = [
        (r'^(.*)$', HelloWorld)
    ]

    def __init__(self, environ, start_response):
        super(WebpyLike, self).__init__(environ, start_response)
        self.request = Request(environ, start_response)


app = WebpyLike


if __name__ == '__main__':
    from colubrid import execute
    execute()
