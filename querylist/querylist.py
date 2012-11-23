from betterdict import BetterDict


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
