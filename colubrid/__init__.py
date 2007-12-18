# -*- coding: utf-8 -*-
"""
=====================
Colubrid WSGI Toolkit
=====================

Colubrid is a WSGI request handler which simplifies python web developement.

If you've ever created a WSGI application without a framework or a request
handler, you know how stupid this can be.

Hello World Example
===================

This example outputs "Hello World"::

    from colubrid import BaseApplication, HttpResponse

    class HelloWorld(BaseApplication):
        def process_request(self):
            return HttpResponse('Hello World!')

    app = HelloWorld

Documentation can be found on `the homepage`_.

.. _the homepage: http://wsgiarea.pocoo.org/colubrid/documentation/
"""
__version__ = '0.10.1'
__author__  = 'Armin Ronacher <armin.ronacher@active-4.com>'
__license__ = 'BSD License'

#from colubrid.application import *
#from colubrid.request import *
#from colubrid.response import *
#from colubrid.server import *
#from colubrid import application
#from colubrid import request
#from colubrid import response
#from colubrid import server

#__all__ = (application.__all__ + request.__all__ + response.__all__ +
#           server.__all__)

from colubrid.application import *
from colubrid.request import Request
from colubrid.response import HttpResponse
from colubrid.server import execute
