import sys

from setuptools import setup, find_packages

from querylist import __version__, __author__

unittest2_module = 'unittest2==0.5.1'

# If we're using Python 3, unittest2 won't work. We need unittest2py3k
if sys.version_info > (3, 0):
    unittest2_module = 'unittest2py3k==0.5.1'

setup(
    name="querylist",
    version=__version__,
    url='https://github.com/thomasw/querylist',
    download_url='https://github.com/thomasw/querylist/downloads',
    author=__author__,
    author_email='thomas.welfley+querylist@gmail.com',
    description='This package provides a QueryList class with django '
                'ORM-esque filtering, excluding, and getting for lists. It '
                'also provides BetterDict, a dot lookup/assignment capable '
                'wrapper for dicts that is 100% backwards compatible.',
    packages=find_packages(),
    tests_require=["nose==1.2.1", "pinocchio==0.3.1", unittest2_module],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries',
    ],
    test_suite='nose.collector'
)
