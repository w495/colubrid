# -*- coding: utf-8 -*-
"""
    Colubrid Object Applications
    
    the following urls will work:
        /                       HelloWorld.index()
        /*/                     HelloWorld.index(*)
        /about                  HelloWorld.about()
        /blog/                  Blog.index()
        /blog/article/*/        Blog.article(*)
        /blog/archive/          Blog.archive()
        /blog/archive/*/        Blog.archive(*)
        /blog/archive/*/*/      Blog.archive(*, *)
        /blog/archive/*/*/*/    Blog.archive(*, *, *)
        /blog/admin/            BlogAdmin.index()
    
    They get automatically mapped to the root object of
    the application.
    Because ModifySlashMiddleware is enabled the application will
    append trailing slashes on it's own.
"""
from colubrid import ObjectApplication, Request
from colubrid.exceptions import AccessDenied
from datetime import datetime


class HelloWorld(object):

    def index(self, name='World'):
        return 'Hello %s from the index page' % name

    def about(self):
        return '<h1>About Hello World</h1><p>...</p>'

    def denied(self):
        raise AccessDenied

    def _private(self):
        # you should never reach this point
        pass


class Blog(object):
    
    def index(self):
        return '<h1>Blog Index</h1>'
        
    def article(self, article_id):
        return '<h1>Article #%s</h1>' % article_id
        
    def archive(self, year=None, month=None, day=None):
        this = datetime.now()
        args = (
            year or this.year,
            month or this.month,
            day or this.day
        )
        return '<h1>Archive</h1><p>For %s/%s/%s</p>' % args
    archive.container = True


class BlogAdmin(object):

    def index(self):
        return '<h1>Blog Admin</h1>'


class DispatcherApplication(ObjectApplication):
    root = HelloWorld
    root.blog = Blog
    root.blog.admin = BlogAdmin

    def __init__(self, environ, start_response):
        super(DispatcherApplication, self).__init__(environ, start_response)
        self.request = Request(environ)
    
app = DispatcherApplication


if __name__ == '__main__':
    from colubrid import execute
    execute()
