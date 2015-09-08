from __future__ import absolute_import

from .betterdict import BetterDict
from .fieldlookup import field_lookup


class QueryList(list):
    """A QueryList is an extension of Python's built in list data structure
    that adds easy filtering, excluding, and retrieval of member objects.

    >>> from querylist import QueryList
    >>> sites = QueryList(get_sites())
    >>> sites.exclude(published=True)
    [{'url': 'http://site3.tld/', 'published': False}]

    Keywrod arguments:

    * data -- an iterable reprsenting the data that to be to queried.
    * wrapper -- a callable that can convert data's elements to objects that
      are compatbile with QueryList
    * wrap -- Boolean toggle to indicate whether or not to call wrapper on
      each element in data on instantiation. Set to false if data's elements
      are already compatible with QueryList.

    """
    def __init__(self, data=None, wrapper=BetterDict, wrap=True):
        """Create a QueryList from an iterable and a wrapper object."""
        self._wrapper = wrapper
        self._wrap = wrap
        self.src_data = data
        converted_data = data or []

        # Wrap our src_data with wrapper
        if self._wrap:
            converted_data = self._convert_iterable(data) if data else []

        super(QueryList, self).__init__(converted_data)

    def __add__(self, y):
        """Return a new QueryList containing itself and the passed iterable.

        Note that addition operations may result in QueryLists with mixed
        wrappers. Consider

        >>> a = QueryList(some_data)
        >>> b = QueryList(some_other_data, wrap=False)
        >>> c = a + b

        The resulting QueryList `c` will contain a mixture of BetterDicts (
        QueryList a's members) and dicts (QueryList b's members) assuming both
        `some_data` and `some_other_data` are lists of dictionaries.

        """
        return QueryList(data=super(QueryList, self).__add__(y), wrap=False)

    @property
    def count(self):
        """Returns the nubmer of objects in the QueryList."""
        return len(self)

    def _convert_iterable(self, iterable):
        """Converts elements returned by an iterable into instances of
        self._wrapper

        """
        # Return original if _wrapper isn't callable
        if not callable(self._wrapper):
            return iterable

        return [self._wrapper(x) for x in iterable]

    def _check_element(self, lookup_strings, instance):
        """Return True if lookup string/value pairs match against the passed
        object.

        """
        for q, val in lookup_strings.items():
            if not field_lookup(instance, q, val, True):
                return False

        return True

    def get(self, **kwargs):
        """Returns the first object encountered that matches the specified
        lookup parameters.

        >>> site_list.get(id=1)
        {'url': 'http://site1.tld/', 'published': False, 'id': 1}
        >>> site_list.get(published=True, id__lt=3)
        {'url': 'http://site1.tld/', 'published': True, 'id': 2}
        >>> site_list.filter(published=True).get(id__lt=3)
        {'url': 'http://site1.tld/', 'published': True, 'id': 2}

        If the QueryList contains multiple elements that match the criteria,
        only the first match will be returned. Use ``filter()`` to retrieve
        the entire set.

        If no match is found in the QueryList, the method will raise a
        ``NotFound`` exception.

        >>> site_list.get(id=None)
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
          File "querylist/querylist.py", line 55, in get
        querylist.querylist.NotFound: Element with specified attributes not
        found.

        """
        for x in self:
            if self._check_element(kwargs, x):
                return x

        raise NotFound("Element with specified attributes not found.")

    def exclude(self, **kwargs):
        """Generates a QueryList containing the subset of objects from
        this QueryList that do **not** match the provided field lookups.

        The following example returns the subset of a QueryList named
        ``site_list`` where the id is greather than 1000.

        >>> site_list.exclude(id__gt=1000)
        [{'url': 'http://site1001.tld/',...}, {...}],

        In the next example, ``exclude()`` returns the subset of objects
        from site_list that aren't published and don't have "test" in their
        title

        >>> site_list.exclude(published=True, title__icontains="test")
        [{'url': 'http://site1.tld/',...}, {...}]

        If all objects match the provided field lookups, then an empty
        QueryList is returned:

        >>> site_list.exclude(id__gt=0)
        []

        """
        return QueryList(
            data=(x for x in self if not self._check_element(kwargs, x)),
            wrapper=self._wrapper, wrap=False)

    def filter(self, **kwargs):
        """Generates a QueryList containing the subset of objects from this
        QueryList that match the provided set of field lookups.

        The following example returns the subset of a QueryList named
        ``site_list`` where published is equal to False:

        >>> site_list.filter(published=True)
        [{'url': 'http://site1.tld/',...}, {...}],

        Similarly, in the next example, ``filter()`` returns the subset of
        objects where object.meta.keywords contains the string 'kittens' and
        where the id property is greater than 100.

        >>> site_list.filter(meta__keywords__contains='kittens', id__gt=100)
        [{'url': 'http://site101.tld/',...}, {...}],

        If no objects match the provided field lookups, an empty QueryList
        is returned.

        >>> site_list.filter(id__gte=1000, published=False)
        []

        """
        return QueryList(
            data=(x for x in self if self._check_element(kwargs, x)),
            wrapper=self._wrapper, wrap=False)


class NotFound(Exception):
    pass
