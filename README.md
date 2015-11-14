# querylist

[![Build Status](https://img.shields.io/travis/thomasw/querylist.svg)](https://travis-ci.org/thomasw/querylist)
[![Coverage Status](https://img.shields.io/coveralls/thomasw/querylist.svg)](https://coveralls.io/r/thomasw/querylist)
[![Latest Version](https://img.shields.io/pypi/v/querylist.svg)](https://pypi.python.org/pypi/querylist/)
[![Downloads](https://img.shields.io/pypi/dm/querylist.svg)](https://pypi.python.org/pypi/querylist/)

Sick of for loop + conditional soup when dealing with complicated lists?
Querylist is here to help.

This package provides a data structure called a QueryList, an extension of
Python's built in list data type that adds django ORM-eseque filtering,
exclusion, and get methods. QueryLists allow developers to easily query and
retrieve data from complex lists without the need for unnecessarily verbose
iteration and selection cruft.

The package also provides BetterDict, a backwards-compatible wrapper for
dictionaries that enables dot lookups and assignment for key values.

Take a look at the [complete
documentation](https://querylist.readthedocs.org/) for more information.

## Installation

Querylist can be installed like any other python package:

    > pip install querylist

Querylist is tested against Python 2.6, 2.7, 3.3, 3.4, and pypy.

## Usage

### BetterDicts

BetterDicts wrap normal dicts. They have all of the same functionality one
would expect from a normal dict:

    >>> from querylist import BetterDict
    >>> src = {'foo': 'bar', 'items': True}
    >>> bd = BetterDict(src)
    >>> bd == src
    True
    >>> bd['foo']
    'bar'
    >>> bd.items()
    [('items', True), ('foo', 'bar')]

However, BetterDicts can also preform dot lookups and assignment of key
values!

    >>> bd.bar_time = True
    >>> bd.foo = 'meh'
    >>> bd.foo
    'meh'
    >>> bd.bar_time
    True
    >>> bd['bar_time']
    True

Key values that conflict with normal dict attributes are accessible via a
`_bd_` attribute.

    >>> bd.items
    <built-in method items of BetterDict object at 0x10d3a7fb0>
    >>> bd._bd_.items
    True

[More about BetterDicts >>](https://querylist.readthedocs.org/en/latest/betterdict.html)

### QueryLists

QueryLists work just like lists:

    >>> from querylist import QueryList
    >>> site_list = [
        {
            'url': 'http://site1.tld/',
            'meta': {
                'keywords': ['Mustard', 'kittens'],
                'description': 'My cool site'
            },
            'published': True,
            'id': 1,
            'name': 'Site 1'
        }, {
            'url': 'http://site2.tld/',
            'meta': {
                'keywords': ['Catsup', 'dogs'],
                'description': 'My cool site'
            },
            'published': True,
            'id': 2,
            'name': 'SitE 2'
        }, {
            'url': 'http://site3.tld/',
            'meta': {
                'keywords': ['Mustard', 'kittens'],
                'description': 'My cool site'
            },
            'published': False,
            'id': 3,
            'name': 'Site 3'
        }
    ]
    >>> ql = QueryList(site_list)
    >>> ql == site_list
    True

They also let developers, exclude objects that don't match criteria via field
lookups or filter the QueryList to only the objects that do match a provided
criteria:

    >>> ql.exclude(published=True)
    [{'url': 'http://site3.tld/', 'meta': {'keywords': ['Mustard', 'kittens'], 'description': 'My cool site'}, 'id': 3, 'name': 'Site 3', 'published': False}]
    >>> ql.filter(published=True).exclude(meta__keywords__contains='Catsup')
    [{'url': 'http://site1.tld/', 'meta': {'keywords': ['Mustard', 'kittens'], 'description': 'My cool site'}, 'id': 1, 'name': 'Site 1', 'published': True}]

And finally, they let developers retrieve specific objects with the get
method:

    >>> ql.get(id=2)
    {'url': 'http://site1.tld/', 'meta': {'keywords': ['Mustard', 'kittens'], 'description': 'My cool site'}, 'id': 2, 'name': 'Site 1', 'published': True}

By default, QueryLists work exclusively with lists of dictionaries. This is
achieved partly by converting the member dicts to BetterDicts on
instantiation. QueryLists also supports lists of any objects that support dot
lookups. `QueryList.__init__()` has parameters that let users easily convert
lists of dictionaries to custom objects. Consider the `site_list` example
above: instead of just letting the QueryList default to a BetterDict, we could
instantiate it with a custom Site class that provides methods for publishing,
unpublishing, and deleting sites. That would then allow us to write code like
the following, which publishes all unpublished sites:

    >>> from site_api import Site
    >>> ql = QueryList(site_list, wrap=Site)
    >>> [x.publish() for x in ql.exclude(published=True)]

[More about QueryLists >>](https://querylist.readthedocs.org/en/latest/querylist.html)

## Contributing

1. Fork the repo and then clone it locally.
2. Install the development requirements: `pip install -r requirements.txt` (
    use `requirements26.txt` for python 2.6)
3. Use [testtube](https://github.com/thomasw/testtube/)'s `stir` command
(installed via #2) to monitor the project directory for changes and
automatically run the test suite.
4. Make changes and submit a pull request.

At the moment, Querylist has great test coverage. Please do your part to help
keep it that way by writing tests whenever you add or change code.

## Everything else

Copyright (c) [Thomas Welfley](http://welfley.me). See
[LICENSE](https://github.com/thomasw/querylist/blob/master/LICENSE) for
details.
