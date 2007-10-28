#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    This file implememts a custom application.
"""
import re
import inspect
from colubrid.request import Request
from colubrid.response import HttpResponse
from colubrid.exceptions import ERROR_PAGE_TEMPLATE, HttpException,\
                                PageNotFound, HttpFound


class Application(object):

    def __init__(self):
        self.mapper = {}

    def register(self, instance):
        for name in dir(instance):
            if name.startswith('_'):
                continue
            ref = getattr(instance, name)
            if inspect.isroutine(ref) and hasattr(ref, 'regexes'):
                for regex in ref.regexes:
                    self.mapper[re.compile(regex)] = ref

    def __call__(self, environ, start_response):
        req = Request(environ, start_response, 'utf-8')
        path = environ.get('PATH_INFO', '/')[1:]
        try:
            for regex, handler in self.mapper.iteritems():
                m = regex.search(path)
                if not m is None:
                    resp = handler(req, *m.groups())
                    break
            else:
                raise PageNotFound()
        except HttpException, e:
            resp = HttpResponse(e.get_error_page(), e.get_headers(), e.code)
        if not isinstance(resp, HttpResponse):
            if isinstance(resp, tuple):
                resp = HttpResponse(*resp)
            else:
                resp = HttpResponse(resp)
        return resp(req)


def expose(*regexes):
    """
    Helper decorator for exporting views.
    """
    def wrapped(f):
        f.regexes = regexes
        return f
    return wrapped


class Pages(object):

    @expose(r'^$')
    def index(self, req):
        return 'Hello World!'

    @expose(r'^downloads/$')
    def downloads(self, req):
        return 'Downloads'

    @expose(r'^downloads$')
    def download_redirect(self, req):
        raise HttpFound('downloads/')

    @expose(r'^downloads/(\d+)$')
    def downloads_detail(self, req, download_id):
        download_id = int(download_id)
        return 'You\'re looking at download "%d".' % download_id


# create a instance for the application and register a set of pages
app = Application()
app.register(Pages())

if __name__ == '__main__':
    from colubrid import execute
    execute(app, reload=True, debug=True)
