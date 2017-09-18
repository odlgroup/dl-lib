# Copyright 2014-2017 The ODL contributors
#
# This file is part of ODL.
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at https://mozilla.org/MPL/2.0/.

"""Setup script for ``deep-learning-library``.

Installation command::

    pip install [--user] [-e] .
"""

from __future__ import print_function, absolute_import

import os
from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand
import sys


root_path = os.path.dirname(__file__)


requires = open(os.path.join(root_path, 'requirements.txt')).readlines()
test_requires = open(
    os.path.join(root_path, 'test_requirements.txt')).readlines()


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


test_path = os.path.join(root_path, 'dllib', 'test')


def find_tests():
    """Discover the test files for packaging."""
    tests = []
    for path, _, filenames in os.walk(os.path.join(root_path, test_path)):
        for filename in filenames:
            basename, suffix = os.path.splitext(filename)
            if (suffix == '.py' and
                    (basename.startswith('test_') or
                     basename.endswith('_test'))):
                tests.append(os.path.join(path, filename))

    return tests


# Determine version from top-level package __init__.py file
with open(os.path.join(root_path, 'dllib', '__init__.py')) as f:
    for line in f:
        if line.startswith('__version__'):
            version = line.strip().split()[-1][1:-1]
            break

setup(
    name='deep-learning-library',

    version=version,

    description='Library of custom add-ons for Deep Learning frameworks',

    url='https://github.com/odlgroup/deep-learning-library',

    author='Jonas Adler, Holger Kohr',
    author_email='odl@math.kth.se',

    license='MPL-2.0',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers

    keywords='research development mathematics prototyping deep-learning',

    packages=find_packages(),
    package_dir={'dllib': 'dllib'},

    install_requires=[requires],
    tests_require=['pytest'],
    extras_require={
        'testing': test_requires,
    },

    cmdclass={'test': PyTest},
)
