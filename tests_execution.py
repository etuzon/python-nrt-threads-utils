import os

from setuptools import find_packages

import nrt_threads_utils
from tests.tests_suite import TestsSuite

PATH = os.path.dirname(__file__)


def __replace_pyproject_packages():
    packages = find_packages()
    packages.remove('tests')

    with open(os.path.join(PATH, 'pyproject.toml')) as f:
        file_lines = [line.strip() for line in f.readlines()]

    is_replace = False

    for i, line in enumerate(file_lines):
        if line.startswith('packages'):
            file_lines[i] = f"packages={packages}"
            is_replace = True
            break

    if is_replace:
        with open(os.path.join(PATH, 'pyproject.toml'), 'w') as f:
            f.write('\n'.join(file_lines))


def __replace_pyproject_version():
    with open(os.path.join(PATH, 'pyproject.toml')) as f:
        file_lines = [line.strip() for line in f.readlines()]

    is_replace = False

    for i, line in enumerate(file_lines):
        if line.startswith('version'):
            version = line.split('=')[1]
            if version != nrt_threads_utils.__version__:
                is_replace = True
                file_lines[i] = f"version='{nrt_threads_utils.__version__}'"
                break

    if is_replace:
        with open(os.path.join(PATH, 'pyproject.toml'), 'w') as f:
            f.write('\n'.join(file_lines))


##################################################################

__replace_pyproject_version()
__replace_pyproject_packages()

test_suite = TestsSuite(True)
test_suite.run_tests()
test_suite.create_report()
test_suite.erase_data()
