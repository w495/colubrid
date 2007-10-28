# -*- coding: utf-8 -*-
"""
    Colubrid Example Wiki
    =====================
"""

import os
import sys
from colubrid import BaseApplication, ResponseRequest
from colubrid.exceptions import PageNotFound, HttpRedirect
from xml.sax import saxutils
from datetime import datetime
import re
import urllib
import time


class Page(object):

    rootpath = os.path.realpath('pages')

    def __init__(self, name, revision=None):
        self.name = name.replace('_', ' ').strip('/')
        if self.name.startswith(' '):
            raise ValueError, 'Invalid Pagename'
        
        if revision is None:
            self.revision = self.get_current_revision()
        else:
            self.revision = revision
        
        self.exists = os.path.exists(self.get_filename())

        try:
            mtime = os.path.getmtime(self.get_filename())
        except:
            self.date = None
        else:
            args = time.localtime(mtime)
            self.date = datetime(*args[:6])
    
   
    def get_current_revision(self):
        try:
            fn = os.path.join(self.rootpath, self.quoted_name, 'revision')
            return int(file(fn).read().strip())
        except IOError:
            return 0
        
    def get_revisions(self):
        result = []
        for file in os.listdir(os.path.join(self.rootpath, self.quoted_name)):
            try:
                result.append(int(file))
            except:
                pass
        result.sort()
        return result[::-1]
                
    def get_filename(self):
        return os.path.join(self.rootpath, self.quoted_name, str(self.revision))

    def save(self, raw):
        pagepath = os.path.join(self.rootpath, self.quoted_name)
        if not os.path.exists(pagepath):
            os.mkdir(pagepath)
        self.revision = self.get_current_revision() + 1
        fn = os.path.join(self.rootpath, self.quoted_name, 'revision')
        file(fn, 'w').write(str(self.revision))
        file(self.get_filename(), 'w').write(raw)
        self.exists = True
        self.date = datetime.now()

    def delete(self):
        self.save('')

    def link(self, request):
        append = '/%s' % urllib.quote(self.name.replace(' ', '_'))
        return request.get_full_url(append)

    def parse(self):
        from textile import textile
        return textile(saxutils.escape(self.raw))
        
    def _get_quoted_name(self):
        from re import sub
        def handle_match(m):
            return '(%s)' % m.group(0)
        name = self.name.replace(' ', '_')
        return sub(r'(\%([A-F0-9]{2}))+', handle_match, name)
    quoted_name = property(_get_quoted_name)
        
    def _get_raw(self):
        if self.exists:
            return file(self.get_filename()).read()
        return ''
    raw = property(_get_raw)

    def get_pagelist(request):
        result = []
        for file in os.listdir(Page.rootpath):
            if not file.startswith('.'):
                result.append(Page(file))
        result.sort()
        return result
    get_pagelist = staticmethod(get_pagelist)


class WikiRequest(ResponseRequest):

    def get_full_url(self, url):
        return '/'.join([self.environ['SCRIPT_ROOT'].rstrip('/'), url.lstrip('/')])


class WikiApplication(BaseApplication):

    def __init__(self, environ, start_response):
        super(WikiApplication, self).__init__(environ, start_response)
        self.request = WikiRequest(environ)

    def process_request(self):
        pagename = self.request.environ.get('PATH_INFO', '/')[1:] or 'Main Page'
        if 'rev' in self.request.args and self.request.args['rev'].isdigit():
            page = Page(pagename, int(self.request.args['rev']))
        else:
            page = Page(pagename)
        
        action = self.request.args.get('action')
        if page.name == 'Pagelist':
            self.show_pagelist()
        elif not action or action == 'show':
            self.show_page(page)
        elif action == 'edit':
            self.edit_page(page)
        elif action == 'delete':
            self.delete_page(page)
        elif action == 'revisions':
            self.show_revisions(page)
        elif action == 'raw':
            self.show_raw(page)

        # each application has to send an response
        # even if it uses the ResponseRequest
        self.request.send_response(None)
    
    def show_pagelist(self):
        self.send_header('Pagelist')
        self.send_navibar()
        self.request.write(
            '<h1>Pagelist</h1>'
            '<p>This is a list of all existing pages:</p>'
            '<ul>'
        )
        for page in Page.get_pagelist(self.request):
            self.request.write('<li><a href="%s">%s</a></li>' % (
                page.link(self.request), saxutils.escape(page.name)))
        self.request.write('</ul>')
        self.send_footer()
    
    def show_page(self, page):
        if not page.exists:
            return self.show_missing(page)
        self.send_header(page.name)
        self.send_navibar(page)
        if page.revision < page.get_current_revision():
            self.request.write(
                '<div class="notice">you\'re looking at version #%d '
                'of this page.</div>' % page.revision
            )
        self.request.write(page.parse())
        self.send_footer()

    def show_raw(self, page):
        self.request.headers['Content-Type'] = 'text/plain; charset=utf-8'
        self.request.write(page.raw)

    def edit_page(self, page):
        if not 'text' in self.request.form:
            self.send_header('Edit Page')
            self.send_navibar(page)
            self.request.write(
                '<h1>%s</h1>'
                '<form action="?action=edit" method="post">'
                '<textarea name="text" rows="10" cols="60">'
                '%s</textarea><br />'
                '<input type="submit" name="save" value="Save Changes" />'
                '<input type="submit" name="cancel" value="Cancel" />'
                '</form>'
                % (
                    saxutils.escape(page.name),
                    saxutils.escape(page.raw)
                )
            )
            self.send_footer()
        else:
            if 'save' in self.request.form:
                from posixpath import join
                page.save(self.request.form.get('text', ''))
            raise HttpRedirect, page.link(self.request)

    def delete_page(self, page):
        if 'yes' in self.request.form:
            page.delete()
            raise HttpRedirect, page.link(self.request)
        elif 'no' in self.request.form:
            raise HttpRedirect, page.link(self.request)
        else:
            self.send_header('Delete Page')
            self.send_navibar(page)
            self.request.write(
                '<form action="?action=delete" method="post">'
                '<h1>Delete Page</h1>'
                '<p>Do you really want to delete the page "%s"?</p>'
                '<p><input type="submit" name="yes" value="Yes" />'
                '<input type="submit" name="no" value="No" /></p>'
                '</form>' % saxutils.escape(page.name)
            )
            self.send_footer()
        
    def show_revisions(self, page):
        self.send_header('Page Revisions')
        self.send_navibar(page)
        self.request.write('<h1>Page Revisions</h1>')
        self.request.write('<ul>')
        for rev in page.get_revisions():
            p = Page(page.name, rev)
            self.request.write('<li><a href="%s?rev=%d">Revision #%d</a> - %s</li>' % (
                p.link(self.request), rev, rev, p.date.strftime('%Y-%m-%d %H:%M')))
        self.request.write('</ul>')
        self.send_footer()
    
    def show_missing(self, page):
        self.send_header(page.name)
        if page.revision > 0:
            self.send_navibar(page)
            append = '&rev=%d' % page.revision
        else:
            self.send_navibar()
            append = ''
        self.request.write(
            '<h1>Page Not Found</h1>'
            '<p>The page "%s" in revison %d does not exists.</p>'
            '<p><a href="?action=edit%s">click here</a> to create it.</a></p>'
            % (saxutils.escape(page.name), page.revision, append)
        )
        self.send_footer()
        
    def send_navibar(self, page=None):
        if not page is None and page.revision > 0 and\
           page.revision < page.get_current_revision():
            rev = '&rev=%d' % page.revision
        else:
            rev = ''
        self.request.write('<ul id="navigation">')
        navibar = [
            (self.request.get_full_url('/Main_Page'), 'Main Page'),
            (self.request.get_full_url('/Pagelist'), 'Pagelist')
        ]
        if not page is None:
            navibar += [
                ('%s?action=edit%s' % (page.link(self.request), rev), 'Edit'),
                ('%s?action=delete' % page.link(self.request), 'Delete'),
                ('%s?action=revisions' % page.link(self.request), 'Revisions'),
                ('%s?action=raw' % page.link(self.request), 'Source')
            ]
        for href, caption in navibar:
            self.request.write('<li><a href="%s">%s</a></li>' % (
                               href, saxutils.escape(caption)))
        self.request.write('</ul>')
        
    def send_header(self, title):
        self.request.write(
            '<?xml version="1.0" encoding="utf-8"?>'
            '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">'
            '<html xmlns="http://www.w3.org/1999/xhtml">'
            '<head>'
            '<title>%(title)s | Demo Wiki</title>'
            '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
            '<link rel="stylesheet" href="%(base)s/_static/screen.css" media="screen" />'
            '<link rel="stylesheet" href="%(base)s/_static/print.css" media="print" />'
            '</head>'
            '<body>'
            '<div id="header"><a href="%(base)s/">Demo Wiki</a></div>'
            % {
                'base': self.request.environ.get('SCRIPT_NAME', '/')[1:],
                'title': saxutils.escape(title)
            }
        )

    def send_footer(self):
        self.request.write('</body></html>')


app = WikiApplication
exports = {
    '/_static': os.path.realpath('shared')
}

if __name__ == '__main__':
    from colubrid import execute
    from paste.evalexception import EvalException
    app = EvalException(app)
    execute()

