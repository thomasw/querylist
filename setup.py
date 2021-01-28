import sys

from setuptools import setup, find_packages

import querylist

setup(
    name='querylist',
    version=querylist.__version__,
    url='https://github.com/thomasw/querylist',
    download_url='https://github.com/thomasw/querylist/downloads',
    author=querylist.__author__,
    author_email='thomas.welfley+querylist@gmail.com',
    description='This package provides a QueryList class with django '
                'ORM-esque filtering, excluding, and getting for lists. It '
                'also provides BetterDict, a dot lookup/assignment capable '
                'wrapper for dicts that is 100% backwards compatible.',
    packages=find_packages(),
    tests_require=['nose>=1.3.7,<1.4', 'spec>=1.4.1,<1.5'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries',
    ],
    test_suite='nose.collector',
)
