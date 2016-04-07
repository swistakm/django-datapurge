# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

from datapurge import __version__ as version

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

try:
    from pypandoc import convert

    def read_md(f):
        return convert(f, 'rst')

except ImportError:
    print(
        "warning: pypandoc module not found, could not convert Markdown to RST"
    )

    def read_md(f):
        return open(f, 'r').read()  # noqa


setup(
    name='django-datapurge',
    version=version,
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',
    description=(
        'A simple Django app to easily handle '
        'cleanup of old data (sessions, nonces, etc.)'
    ),
    long_description=read_md('README.md'),
    url='https://github.com/swistakm/django-datapurge',
    author = 'Michał Jaworski',
    author_email = 'swistakm@gmail.com',
    classifiers = [
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.4',
        'Framework :: Django :: 1.5',
        'Framework :: Django :: 1.6',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    test_suite='datapurge.runtests.runtests.main',
)

