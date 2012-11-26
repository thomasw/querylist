QueryList
=========

.. autoclass:: querylist.QueryList

Instantiation
-------------

By default, QueryLists expect to be instantiated with lists of dictionaries
or dictionary-like data because it attempts to convert the elements to
BetterDicts:

>>> a = QueryList([{'foo': 1}, {'foo': 2}])
>>> b = QueryList([(('foo', 1),),(('foo', 2),) ])
>>> a == b
True
>>> a.get(foo__lt=2)
{'foo': 1}

Fortunately, QueryLists can also be instantiated with iterables returning any
objects that support dot lookups. To invoke a QueryList with a custom wrapper
called ``myclass``, one could write the following:

>>> c = QueryList(mydata, wrapper=myclass, wrap=False)

``wrap=False`` in the above examples tells the QueryList that it doesn't
need to convert the elements of mydata to myclass. If wrap had been true,
something similar to ``[myclass(x) for x in mydata]`` would have been
executed.

If ``mydata`` had been a list of data that can be converted to a custom
object, then ``wrap=True`` (the default behavior) would have been appropriate.

>>> d = QueryList(mydata, wrapper=myclass)

``wrapper`` can be any callable that returns a QueryList compatible object.
It doesn't need to be a class.

It is also possible to instantiate an empty QueryList and add objects to it
as needed:

>>> a = QueryList()

Querying
--------

All objects
^^^^^^^^^^^

You can iterate over a QuerySet like a normal list and it will return the data
that was used to instantiate it (the data will be wrapped, if ``wrapped=True``
when the list was instantiated).

>>> a = QueryList(my_data)
>>> [item for item in a]

Limiting and Excluding
^^^^^^^^^^^^^^^^^^^^^^

QueryLists provide two methods for limiting and excluding objects from a
QueryList: ``limit()`` and ``exclude()``. ``limit()`` will return a QueryList
containing all objects in the list that match the passed conditions, and
``exclude()`` will return a QueryList containing the subset of the original
QueryList that doesn't match the passed conditions.

Both methods accept keyword argument/value pairs, where the keyword is a field
lookup and the value is the value to compare that field to. For example,
``id=4`` would match all objects with an id property equal to 4. See
:ref:`field_lookups` for more information.

.. automethod:: querylist.QueryList.limit
.. automethod:: querylist.QueryList.exclude

Chaining
^^^^^^^^

QueryList methods that return QueryLists  (`limit()` and `exclude()`) can be
chained together to form more complex queries:

>>> QueryList(sites).include(published=False).exclude(meta__keywords__contains="kittens")
[]

Retrieving a single object
^^^^^^^^^^^^^^^^^^^^^^^^^^

In addition to providing methods for limiting or excluding objects, QueryLists
provide a method for retrieving specific objects:

.. automethod:: querylist.QueryList.get

.. _field_lookups:

Field lookups
-------------

A field lookup consists of a name corresponding to an object attribute and
a value to compare that attribute against. The following is a field lookup
for all QueryList object whose id property is equal to 1000: ``id=1000``.

Similarly, ``title="Go Team!"`` would match all objects with the title team.

Field lookups can be combined arbitrarily: ``id=1000, title="Go team!"`` would
match all objects with the id 1000 and the title "Go Team!".

Properties of properties
^^^^^^^^^^^^^^^^^^^^^^^^

Field lookups can extend to properties of properties (and so on). Simply
replace the dot operator that one would normally use with a double underscore.
``meta__description="Cats"``, for example, would match against all objects in
the QueryList where object.meta.description=="Cats."

Similarly, ``meta__keywords__count=4`` would match against all objects in the
QueryList where object.meta.keywords.count==4.

Comparators
^^^^^^^^^^^

Field lookups can end with an optional comparator designation that indicates
that the lookup should do something other than an exact comparison:
``attribute__<comparator>``.

A field lookup that does a case insensitive match against the title attribute
would look like: ``title__iexact="cats"``.

Querylist ships with a number of comparators:

**exact**

Returns True if the attribute and the specified value are equal.

**iexact**

Converts both the attribute and the specified value to lowercase and returns
True if the values are equal.

Both the attribute and the specified value must be strings.

**contains**

Returns True if the specified value is ``in`` the attribute value. This
works with strings and lists.

**icontains**

Converts both the attribute and the specified value to lowercase and returns
True if the specified value is ``in`` the attribute value.

**in**

Returns True if the attribute is ``in`` the specified iterable

This requires the specified value to be some iterable.

**startswith**

Returns true if the attribute value starts with the specified value.

This requires the attribute value and specified value to be strings.

**istartswith**

Case insensitive startswith.

**endswith**

Returns true if the attribute value ends with the specified value.

This requires the attribute value and specified value to be strings.

**iendswith**

Case insensitive endswith.

**regex**

Returns True if the attribute value matches the specified regular expression.

**iregex**

Case insensitive regex.

**gt**

Returns True if the attribute value is greater than the specified value.

**gte**

Returns True if the attribute value is greater than or equal to the specified
value.

**lt**

Returns True if the attribute value is less than the specified valued.

**lte**

Returns True if the attribute value is less than or equal to the specified
value.

Aggregation
-----------

.. autoattribute:: querylist.QueryList.count

Backwards compatibility
-----------------------

QueryLists are intended to be a drop in replacement for lists of dictionaries.
Because QueryLists and their default wrapper (BetterDicts) are backwards
compatible with lists and dicts respectively, a developer can drop them into
existing projects without changing the existing behavior.

Consider a user class that returns a list of sites::

    class User(object):
        def get_sites():
            """Returns a list of the user's sites."""
            return Site(self.id).get_all_sites()

If dictionaries are being used to represent sites, we can change the definition
of ``get_sites()`` as follows without impacting any existing functionality::

    def get_sites():
        """Returns a list of the user's sites."""
        return QueryList(Site(self.id).get_all_sites())

The new ``get_sites()`` will be backwards compatible with its old definition,
but for any new code written, the developer can use QueryList and BetterDict
functionality to their heart's content.
