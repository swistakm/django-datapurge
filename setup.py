# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

from datapurge import __version__ as version

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name = 'django-datapurge',
    version = version,
    packages = find_packages(),
    include_package_data = True,
    license = 'BSD License',
    description = 'A simple Django app to easily handle cleanup of old data (sessions, nonces, etc.)',
    long_description = README,
#    url = 'http://www.example.com/',
    author = 'Michał Jaworski',
    author_email = 'swistakm@gmail.com',
    classifiers = [
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    test_suite='datapurge.runtests.runtests.main',
)

