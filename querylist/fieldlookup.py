class FieldLookup(object):
    def __init__(self):
        self.default_comparator = FieldLookup._exact
        self.comparators = {
            'exact': FieldLookup._exact,
            'iexact': FieldLookup._iexact,
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
    def _exact(value1, value2):
        """Compare two values."""
        return value1 == value2

    @staticmethod
    def _iexact(value1, value2):
        """Convert two values to lowercase and compare them."""
        return value1.lower() == value2.lower()


field_lookup = FieldLookup()
