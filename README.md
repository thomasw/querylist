# querylist [![Build Status](https://travis-ci.org/thomasw/querylist.png)](https://travis-ci.org/thomasw/querylist)

Sick of for loop + conditional soup when dealing with complicated lists?
Querylist is here to help.

This library provides a data structure called a QueryList, an extension of
Python's built in list data type that adds django ORM-eseque filtering,
exclusion, and get methods. QueryLists allow developers to easily query and
retrieve data from complex lists without the need for unnecessarily verbose
iteration and selection cruft.

Querylist also provides BetterDict, a backwards-compatible wrapper for
dictionaries that enables dot lookups and assignment for key values.

## Installation

Install Querylist like you'd install any other Python package:

    > pip install querylist

Querylist is tested against Python >2.5, <3.0.

## Usage

### BetterDict

BetterDicts wrap normal dicts. They have all of the same functionality you'd
expect from a normal dict:

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

### QueryList

## Contributing

1. Fork the repo and then clone it locally.
2. Install the development requirements: `pip install -r requirements.txt`
3. Use [testtube](https://github.com/thomasw/testtube/)'s `stir` command
(installed via #2) to monitor the project directory for changes and
automatically run the test suite.
4. Make your changes and submit a pull request.

At the moment, Querylist has great test coverage. Please do your part to help
keep it that way by writing tests whenever you add or change code.

## Everything else

Copyright (c) [Thomas Welfley](http://welfley.me). See
[LICENSE](https://github.com/thomasw/querylist/blob/master/LICENSE) for
details.
