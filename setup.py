# -*- coding: utf-8 -*-
"""Setup file for easy installation"""
from os.path import join, dirname
from setuptools import setup


version = __import__('paginator_plus').__version__

LONG_DESCRIPTION = """
Want to save the url params and get a format page_range?

This package save extra data to django paginator. Useful when url has params.

`http://myhost/something?page=10&a=1 --> [?page=8&a=1, ?page=9&a=1, ?page=10&a=1, ?page=11&a=1, ?page=12&a=1]`
"""


def long_description():
    """Return long description from README.md if it's present
    because it doesn't get installed."""
    try:
        return open(join(dirname(__file__), 'README.md')).read()
    except IOError:
        return LONG_DESCRIPTION


setup(name='django-paginator-plus',
      version=version,
      author='duoduo369',
      author_email='duoduo3369@gmail.com',
      description='Want to save the url params and get a format page_range?'
                  'This package save extra data to django paginator. Useful when url has params.',
      license='MIT',
      keywords='django, paginator',
      url='https://github.com/duoduo369/django-paginator-plus',
      download_url='https://github.com/duoduo369/django-paginator-plus/archive/v0.2.0.tar.gz',
      packages=['paginator_plus'],
      long_description=long_description(),
      install_requires=['Django>=1.4',],
      classifiers=['Framework :: Django',
                   'Development Status :: 4 - Beta',
                   'Topic :: Internet',
                   'License :: OSI Approved :: MIT License',
                   'Intended Audience :: Developers',
                   'Environment :: Web Environment',
                   'Programming Language :: Python :: 2.7'],
      zip_safe=False)
