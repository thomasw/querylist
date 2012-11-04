# Attribute prefix for allowing dotlookups when keys conflict with dict
# attributes.
PREFIX = '_bd_'


class BetterDict(dict):
    def __init__(self, *args, **kwargs):
        # Prefix that will be appended to keys for dot lookups that would
        # otherwise conflict with dict attributes.
        self.__prefix = PREFIX

        # Determine the attributes a dictionary has. We use this to prevent
        # exposing properties that conflict with a dict's properties
        self.__dict_attrs = dir(dict)

        return super(BetterDict, self).__init__(*args, **kwargs)

    def __getattr__(self, attr):
        # Don't attempt lookups for things that conflict with dict attrs
        if attr in self.__dict_attrs:
            raise AttributeError

        # If the requested attribute is prefixed with self.__prefix,
        # we need to unprefix it and do a lookup for that key.
        if attr.startswith(self.__prefix) and attr != self.__prefix:
            unprefixed_attr = attr.partition(self.__prefix)[-1]

            if unprefixed_attr in self and (
                    unprefixed_attr in self.__dict_attrs or
                    unprefixed_attr.startswith(self.__prefix)):
                return self.__dict_to_BetterDict(self[unprefixed_attr])

        if attr in self:
            return self.__dict_to_BetterDict(self[attr])

        raise AttributeError

    def __dict_to_BetterDict(self, value):
        """Convert the passed value to a BetterDict if the value is a dict"""
        return BetterDict(value) if type(value) == dict else value
