import ast
import re
import sys

from setuptools import setup, find_packages

unittest2_module = 'unittest2>=0.5.1,<0.6'

# If we're using Python 3, we don't need unittest2.
if sys.version_info > (3, 0):
    unittest2_module = ''

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('querylist/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

setup(
    name='querylist',
    version=version,
    url='https://github.com/thomasw/querylist',
    download_url='https://github.com/thomasw/querylist/downloads',
    author='Thomas Welfley',
    author_email='thomas.welfley+querylist@gmail.com',
    description='This package provides a QueryList class with django '
                'ORM-esque filtering, excluding, and getting for lists. It '
                'also provides BetterDict, a dot lookup/assignment capable '
                'wrapper for dicts that is 100% backwards compatible.',
    packages=find_packages(),
    tests_require=[
        'nose>=1.3.6,<1.4',
        'spec>=1.2.2,<1.3',
        unittest2_module],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries',
    ],
    test_suite='nose.collector',
)
