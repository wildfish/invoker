from __future__ import print_function, division

import glob
import os
import io
import re
import shutil
import sys
import tarfile
from contextlib import contextmanager
from distutils.log import INFO, WARN, ERROR
from distutils.spawn import find_executable
from tempfile import mkdtemp
from time import sleep

from setuptools import find_packages, setup, Command

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))


def get_readme():
    with io.open(os.path.join(SCRIPT_DIR, 'README.rst'), encoding='utf-8') as readme:
        return readme.read()


def get_install_requirements():
    with io.open(os.path.join(SCRIPT_DIR, 'requirements-package.in'), encoding='utf-8') as reqs:
        return reqs.readlines()


def get_version():
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    with io.open(os.path.join(SCRIPT_DIR, 'invoker', '__init__.py'), encoding='utf-8') as init_py:
        return re.search('__version__ = [\'"]([^\'"]+)[\'"]', init_py.read()).group(1)


version = get_version()
reqs = get_install_requirements()
readme = get_readme()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(
    name='invoker',
    version=version,
    packages=find_packages(exclude=('tests', 'tests.*', 'tests.*.*')),
    include_package_data=True,
    package_data={
        '': [
            'requirements-package.in',
            'LICENSE',
        ],
    },
    exclude_package_data={
        '': ['__pycache__', '*.py[co]'],
    },
    license='BSD 3-Clause',
    description='A wrapper around invoke to help facilitate sharing tasks and specifying multiple environments',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/wildfish/invoker',
    author='Wildfish',
    author_email='Wildfish <developer@wildfish.com>',
    keywords='invoke invoker',
    install_requires=reqs,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
