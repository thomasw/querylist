BetterDict
==========

A BetterDict is a data structure that is backwards compatible with Python's
built in dict type. It has all of the usual dict methods and can still preform
index based lookup and assignment of key values. Even an equal to comparison
of a BetterDict instance invoked with the same data as a dict instance will
evaluate to true.

In addition to standard dict functionality,
BetterDicts also allows dot lookup and assignment of key values.

    >>> from querylist import BetterDict
    >>> a = BetterDict()
    >>> b = dict()
    >>> a.cats = 18
    >>> a['dogs'] = 372
    >>> a.hedgehogs = 19
    >>> b['cats'] = 18
    >>> b['dogs'] = 372
    >>> b['hedgehogs'] = 19
    >>> a == b
    True
    >>> dir(a)
    ['__class__', '__cmp__', '__contains__', '__delattr__', '__delitem__',
     '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__',
     '__getitem__', '__gt__', '__hash__', '__init__', '__iter__', '__le__',
     '__len__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__',
     '__repr__', '__setattr__', '__setitem__', '__sizeof__', '__str__',
     '__subclasshook__', 'cats', 'clear', 'copy', 'dogs', 'fromkeys', 'get',
     'has_key', 'hedgehogs', 'items', 'iteritems', 'iterkeys', 'itervalues',
     'keys', 'pop', 'popitem', 'setdefault', 'update', 'values']

Dot lookups and assignments
---------------------------

Dot lookups that correspond to keys will return the key's value

    >>> foo = BetterDict()
    >>> foo['yay'] = 1
    >>> foo.yay
    1

An assignment will update that key's value:

    >>> foo.yay = 0
    >>> foo['yay']
    0

Assignment of an attribute that has not yet been added as a key to the
BetterDict will add the key/value pair.

    >>> foo.yeah = True
    >>> foo['yeah']
    True

However, a lookup for an attribute that is neither a key nor a normal dict
attribute will raise an ``AttributeError``:

    >>> foo.bar
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "querylist/betterdict.py", line 6, in __getattr__
        raise AttributeError
    AttributeError

Nested Dictionaries
-------------------

A nested dictionary's keys are also accessible via dot lookup. BetterDict
achieves this by converting member dicts to BetterDicts:

Consider the following BetterDict definition:

    >>> c = BetterDict({
    ...     'foo': 1,
    ...     'bar': {
    ...         'a': 0,
    ...         'b': 1,
    ...         'c': 2,
    ...         'another': {
    ...             'd': 0,
    ...             'e': 1,
    ...             'f': 2,
    ...         }
    ...     },
    ... })

``c.bar`` will return the BetterDict at ``c['bar']``:

    >>> c.bar
    {'a': 0, 'c': 2, 'b': 1, 'another': {'e': 1, 'd': 0, 'f': 2}}

Similarly, ``c.bar.another.d`` will descend down to
``c['bar']['another']['d']`` and an assignment using the same identifier chain
will update that value:

    >>> c.bar.another.d
    0
    >>> c.bar.another.d = True
    >>> c.bar.another
    {'e': 1, 'd': True, 'f': 2}

Resolving key name / dict attribute conflicts (the ``_bd_`` attribute)
-----------------------------------------------------------------------

When a BetterDict has a key that conflicts with the name of a standard dict
attribute, the BetterDict does not overwrite the standard attribute. Doing so
would break backwards compatibility for BetterDicts with specific key/value
pairs.

    >>> problem = BetterDict({'update': '3 days ago'})
    >>> problem.update
    <built-in method update of BetterDict object at 0x7fb9f047b610>
    >>> problem['update']
    '3 days ago'

As a work around for this issue, all BetterDicts have an attribute named
``_bd_``, which is protected from being overwritten just like standard dict
attributes. The ``_bd_`` attribute allows dot lookup and assignment of all a
BetterDict's keys regardless of whether or not their name conflicts with a
dict attribute.

    >>> problem._bd_.update
    '3 days ago'
    >>> problem._bd_.update = '4 days ago'
    >>> problem['update']
    '4 days ago'
