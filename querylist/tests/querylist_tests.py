import unittest2

from querylist import QueryList, BetterDict


class QueryListInstantiationTests(unittest2.TestCase):
    """QueryList instantiation"""
    def test_sets_wrapper_attribute_to_BetterDict_by_default(self):
        self.assertEqual(QueryList()._wrapper, BetterDict)

    def test_sets_wrapper_attribute_to_value_passed_as_wrapper_to_init(self):
        self.assertEqual(QueryList(wrapper=dict)._wrapper, dict)

    def test_sets_src_data_attirbute_to_iterable_passed_to_constructor(self):
        self.assertEqual(QueryList([1, 2], None).src_data, [1, 2])

    def test_converts_src_data_members_to_wrapper_type(self):
        self.assertEqual(QueryList([1, 2, 3], str), ['1', '2', '3'])


class QueryListConverIterableTests(unittest2.TestCase):
    """QueryList _convert_iterable"""
    def setUp(self):
        self.iterable = [{'foo': 1}, {'bar': 2}]
        self.ql = QueryList()

    def test_converts_an_iterables_members_to_BetterDicts_by_default(self):
        converted = self.ql._convert_iterable(self.iterable)
        self.assertEqual(converted[0], BetterDict(self.iterable[0]))

    def test_doesnt_convert_an_iterable_when_wrapper_attr_is_None(self):
        ql = QueryList(wrapper=None)
        self.assertEqual(ql._convert_iterable(self.iterable), self.iterable)
