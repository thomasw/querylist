class BetterDict(dict):
    def __getattr__(self, attr):
        if attr in self:
            return self.__dict_to_BetterDict(attr)

        raise AttributeError

    def __dict_to_BetterDict(self, attr):
        """Convert the passed attr to a BetterDict if the value is a dict

        Returns: The new value of the passed attribute."""
        if type(self[attr]) == dict:
            self[attr] = BetterDict(self[attr])

        return self[attr]

    @property
    def _bd_(self):
        """Property that allows dot lookups of otherwise hidden attributes."""
        if not getattr(self, '__bd__', False):
            self.__bd = BetterDictLookUp(self)

        return self.__bd

    def __setattr__(self, attr, value):
        """Write dot assignments to dict keys."""
        self[attr] = value


class BetterDictLookUp(object):
    """Allows dot lookup and assignment of a provided dictionaries keys.

    This class is not backwards compatible with dictionaries."""
    def __init__(self, lookup_dict):
        self._lookup_dict = lookup_dict

    def __getattr__(self, attr):
        try:
            return self._lookup_dict[attr]
        except KeyError:
            raise AttributeError

    def __setattr__(self, attr, value):
        if attr != '_lookup_dict':
            self._lookup_dict[attr] = value

        return super(BetterDictLookUp, self).__setattr__(attr, value)
