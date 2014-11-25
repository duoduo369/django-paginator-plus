# -*- coding: utf-8 -*-
"""Setup file for easy installation"""
from os.path import join, dirname
from setuptools import setup


version = __import__('paginator_plus').__version__

LONG_DESCRIPTION = """django paginator plus"""


def long_description():
    """Return long description from README.rst if it's present
    because it doesn't get installed."""
    try:
        return open(join(dirname(__file__), 'README.me')).read()
    except IOError:
        return LONG_DESCRIPTION


setup(name='django-paginator-plus',
      version=version,
      author='duoduo369',
      author_email='duoduo3369@gmail.com',
      description='Django paginator plus',
      license='MIT',
      keywords='django, paginator',
      url='https://github.com/duoduo369/django-paginator-plus',
      download_url='https://github.com/duoduo369/django-paginator-plus/archive/v0.1.tar.gz',
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
