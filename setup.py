from pathlib import Path

from setuptools import setup, find_packages

import querylist

with open(Path(__file__).absolute().parent / 'README.md', encoding='utf-8') as f:
    long_description = f.read()

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
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    tests_require=['nose>=1.3.7,<1.4', 'spec>=1.4.1,<1.5'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    test_suite='nose.collector',
)
