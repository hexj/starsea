#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import re

try:
    import setuptools

    setup = setuptools.setup
except ImportError:
    setuptools = None
    from distutils.core import setup

def read(*names, **kwargs):
    return io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ).read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


packages = setuptools.find_packages(
    exclude=["*.tests", "*.tests.*", "tests.*", "tests"])
# print(packages)

setup(
    name='starsea',
    version=find_version("styxsdk/__init__.py"),
    description='Styx Resource Storage SDK',
    long_description='see:\nhttps://github.com/hexj/starsea\n',
    author='iqaunt.cn',
    author_email='hexiaojiao@gmail.com',
    maintainer_email='hexiaojiao@gmail.com',
    license='MIT',
    url='https://github.com/hexj/starsea',
    platforms='any',
    packages=['starsea']    # packages=packages,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    install_requires=['requests', 'pycryptodome', 'pywebhdfs',
                      'scikit-learn >= 0.20.1',
                      'numpy >= 1.14.3',
                      'python-docx >= 0.8.7',
                      'matplotlib == 2.2.2',
                      'pandas >= 0.24.0',
                      ],
    entry_points={
        'console_scripts': [
            'styxpy = starsea.main:main',
        ],
    }
)
