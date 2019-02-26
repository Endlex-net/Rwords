#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
from setuptools import setup, find_packages

PROJ_NAME = 'rwords'
PACKAGE_NAME = 'rwords'
VERSION = __import__(PACKAGE_NAME).__version__
PROJ_METADATA = '{}.json'.format(PACKAGE_NAME)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

with open("README.md", "r") as fh:
    README = fh.read()

INSTALL_REQUIRES = ['docopt', 'requests>2.0', 'sqlalchemy>=1.2', 'readchar', 'pygame>=1.6']
if sys.version_info < (3, 0):
    INSTALL_REQUIRES.append('enum34')

setup(
    name=PROJ_NAME,
    version=VERSION,
    description='Rwords: A command line tool to help you remember words faster.',
    long_description=README,
    author='endlex',
    author_email="endlex@aliyun.com",
    license='MIT',
    packages=find_packages(exclude=('tests',)),
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    py_modules=['rwords'],
    install_requires=INSTALL_REQUIRES,

    entry_points={
        'console_scripts': [
            'rw=rwords.rw:main',
        ],
    },
)
