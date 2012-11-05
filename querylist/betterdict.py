class BetterDict(dict):
    def __getattr__(self, attr):
        if attr in self:
            return self.__dict_to_BetterDict(self[attr])

        raise AttributeError

    def __dict_to_BetterDict(self, value):
        """Convert the passed value to a BetterDict if the value is a dict"""
        return BetterDict(value) if type(value) == dict else value

    @property
    def _bd_(self):
        """Property that allows dot lookups of otherwise hidden attributes."""
        if not getattr(self, '__bd__', False):
            self.__bd = BetterDictLookUp(self)

        return self.__bd


class BetterDictLookUp(object):
    def __init__(self, lookup_dict):
        self._lookup_dict = lookup_dict

    def __getattr__(self, attr):
        try:
            return self._lookup_dict[attr]
        except KeyError:
            raise AttributeError
