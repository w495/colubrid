# -*- coding: utf-8 -*-
"""
    Colubrid Setup
"""
import ez_setup
ez_setup.use_setuptools()
import colubrid
from setuptools import setup


setup(
    name = 'Colubrid',
    version = colubrid.__version__,
    url = 'http://wsgiarea.pocoo.org/colubrid/',
    download_url = 'http://wsgiarea.pocoo.org/colubrid/dist/Colubrid-%s.tar.gz' % colubrid.__version__,
    license = colubrid.__license__,
    author = 'Armin Ronacher',
    author_email = 'armin.ronacher@active-4.com',
    description = 'simple wsgi publisher',
    long_description = colubrid.__doc__,
    keywords = 'wsgi web',
    packages = ['colubrid'],
    platforms = 'any',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'License :: OSI Approved :: %s' % colubrid.__license__,
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content'
    ]
)
