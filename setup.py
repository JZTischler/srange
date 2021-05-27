#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os
import sys

import versioneer


version = versioneer.get_version()
license='Argonne National Laboratory Open-Source License'
long_description = '''
This class provides functions to convert a string representing integers and
ranges of integers to an object which can be iterated over all the values
contained in the string and a list of individual values or subranges can be
retrieved.
'''
# remove newlines from long_description
long_description = long_description.replace("\n", " ")


setup(
	name='srange',
	version=version,
	cmdclass=versioneer.get_cmdclass(),
	license=license,
	description='Class to express integer ranges in a string format',
	long_description=long_description,
	author='Jon Tischler, Christian M. Schlepuetz',
	author_email='tischler@aps.anl.gov',
	url='https://github.com/schlepuetz/srange',
	download_url='no-URL-yet',
	platforms='any',
	test_suite="tests",
	package_dir={'': '.'},
	packages=find_packages('.'),
	requires=['numpy'],
	classifiers=[
	    'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering'
    ],
)
