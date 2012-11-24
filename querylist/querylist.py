from betterdict import BetterDict
from fieldlookup import field_lookup


class QueryList(list):
    def __init__(self, data=None, wrapper=BetterDict):
        """Create a QueryList from an iterable and a wrapper object."""
        self._wrapper = wrapper
        self.src_data = data

        # Wrap our src_data with wrapper
        converted_data = self._convert_iterable(data) if data else []

        super(QueryList, self).__init__(converted_data)

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
        for q, val in lookup_strings.iteritems():
            if not field_lookup(instance, q, val, True):
                return False

        return True

    def get(self, **kwargs):
        """Returns the first object encountered that matches the specified
        lookup parameters.

        Raises NotFound if no matching object is found.

        """
        for x in self:
            if self._check_element(kwargs, x):
                return x

        raise NotFound("Element with specified attributes not found.")


class NotFound(Exception):
    pass
