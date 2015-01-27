import re


class FieldLookup(object):
    def __init__(self):
        self.default_comparator = FieldLookup.exact
        self.comparators = {
            'exact': FieldLookup.exact,
            'iexact': FieldLookup.iexact,
            'contains': FieldLookup.contains,
            'icontains': FieldLookup.icontains,
            'in': FieldLookup.isin,
            'startswith': FieldLookup.startswith,
            'istartswith': FieldLookup.istartswith,
            'endswith': FieldLookup.endswith,
            'iendswith': FieldLookup.iendswith,
            'regex': FieldLookup.regex,
            'iregex': FieldLookup.iregex,
            'gt': FieldLookup.gt,
            'gte': FieldLookup.gte,
            'lt': FieldLookup.lt,
            'lte': FieldLookup.lte,
            'call': FieldLookup.call
        }

    def __call__(self, instance, lookup, compare_value=None, compare=False):
        """Return lookedup value or compares it against another.

        Keyword arguments:
        instance -- the instsance to preforma a lookup against
        lookup -- a string representing a chain of lookups to preform
        compare_value -- a value to compare the lookedup value against
        compare -- bool describing whether to preform a lookup or a comparison

        """
        lookup_chain, comparator = self._parse_lookup_string(lookup)
        value = self._resolve_lookup_chain(lookup_chain, instance)

        if not compare:
            return value

        return comparator(value, compare_value)

    def _parse_lookup_string(self, lookup_chain):
        """Convert a lookup string to a (lookup_chain, comparator) tuple."""
        lookup_chain = lookup_chain.split('__')
        comparator = self.default_comparator

        # Only look for a lookup method if the lookup chain is larger than 1
        if len(lookup_chain) <= 1:
            return lookup_chain, comparator

        # Get the correct lookup_method if the last value in the lookup
        # chain is a lookup method specifier
        if lookup_chain[-1] in self.comparators:
            comparator = self.comparators.get(lookup_chain.pop(-1))

        return lookup_chain, comparator

    def _resolve_lookup_chain(self, chain, instance):
        """Return the value of inst.chain[0].chain[1].chain[...].chain[n]."""
        value = instance

        for link in chain:
            value = getattr(value, link)

        return value

    @staticmethod
    def exact(value1, value2):
        """Compare two values."""
        return value1 == value2

    @staticmethod
    def iexact(value1, value2):
        """Convert two values to lowercase and compare them.

        This method requires strings.

        """
        return value1.lower() == value2.lower()

    @staticmethod
    def contains(value1, value2):
        """Return true if the first value contains the second value."""
        return value2 in value1

    @staticmethod
    def icontains(value1, value2):
        """Returns true if the lowercase version of the first value contains
        the lowercase version of the second value.

        This method requires strings.

        """
        return value2.lower() in value1.lower()

    @staticmethod
    def isin(value1, value2):
        """Returns true if the second value contains the first value."""
        return value1 in value2

    @staticmethod
    def startswith(value1, value2):
        """Returns true if the first value starts with the second.

        This method requires strings.

        """
        return value1.startswith(value2)

    @staticmethod
    def istartswith(value1, value2):
        """Returns true if the lowercased first value starts with the
        lowercased second value.

        This method requires strings.

        """
        return value1.lower().startswith(value2.lower())

    @staticmethod
    def endswith(value1, value2):
        """Returns true if the first value ends with the second value."""
        return value1.endswith(value2)

    @staticmethod
    def iendswith(value1, value2):
        """Returns true if the lowercased first value ends with the lowercased
        second value.

        This method requires strings.
        """
        return value1.lower().endswith(value2.lower())

    @staticmethod
    def regex(value, regex):
        """Returns True if the value matches against the regex."""
        return re.match(regex, value)

    @staticmethod
    def iregex(value, iregex):
        """Returns true if the value case insentively matches agains the
        regex.

        """
        return re.match(iregex, value, flags=re.I)

    @staticmethod
    def gt(value1, value2):
        """Returns true if the first value is greater than the second."""
        return value1 > value2

    @staticmethod
    def gte(value1, value2):
        """Returns ture if the first value is greater than or equal to the
        second.

        """
        return value1 >= value2

    @staticmethod
    def lt(value1, value2):
        """Returns true if first value is less than the second."""
        return value1 < value2

    @staticmethod
    def lte(value1, value2):
        """Returns true if the first value is less than or equal to the
        second.

        """
        return value1 <= value2

    @staticmethod
    def call(value1, value2):
        """Return output of callable value2 resulting from passing value1."""
        return value2(value1)


class FieldLookupCollection(object):

    """A collection of field lookup strings.

    FieldLookupCollection(**kwargs) -> new FieldLookUpCollection

    Field lookups should be specified as keyword arguments.

    """

    def __init__(self, **kwargs):
        self._lookup_set = kwargs

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        lookup_string = ''

        for key, value in self._lookup_set.iteritems():
            lookup_string += "%s=%s, " % (key, value)

        return "<Lookups: %s>" % lookup_string.rstrip(', ')

    def evaluate(self, instance):
        """Evaluate the collection of lookups against the passed instance.

        If all lookups return True, then evaluate will return True. If any are
        False, it will return False.

        """
        for q, val in self._lookup_set.iteritems():
            if not field_lookup(instance, q, val, True):
                return False

        return True


field_lookup = FieldLookup()
