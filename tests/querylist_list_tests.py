from unittest import TestCase

from querylist import BetterDict, QueryList


class QueryListAddition(TestCase):
    """QueryList Addition"""

    def setUp(self):
        self.src_list1 = [{"foo": 1}, {"foo": 2}, {"foo": 3}]
        self.src_list2 = [{"foo": 4}, {"foo": 5}, {"foo": 6}]
        self.ql1 = QueryList(self.src_list1)
        self.ql2 = QueryList(self.src_list2, wrap=False)

        self.combined = self.ql1 + self.ql2
        self.all_wrapped = self.ql1 + QueryList(self.src_list2)
        self.ql_and_list = self.ql1 + self.src_list2

    def test_yields_a_QueryList_when_a_list_is_added_to_a_QueryList(self):
        self.assertIsInstance(self.combined, QueryList)

    def test_yields_a_QueryList_when_a_QueryList_is_added_to_a_QueryList(self):
        self.assertIsInstance(self.ql_and_list, QueryList)

    def test_does_not_interfere_with_existing_item_wrappers(self):
        # Element from the first QL
        self.assertEqual(type(self.combined[0]), BetterDict)
        # Element from the second
        self.assertEqual(type(self.combined[-1]), dict)

    def test_yields_QueryList_containing_both_lists(self):
        self.assertEqual(self.src_list1 + self.src_list2, self.combined)

    def test_with_list_contains_original_QueryList_and_list(self):
        self.assertEqual(self.src_list1 + self.src_list2, self.ql_and_list)

    def test_doesnt_break_filtering_capabilities(self):
        self.assertEqual(
            self.all_wrapped.filter(foo__call=lambda x: x % 2 == 0),
            [{"foo": 2}, {"foo": 4}, {"foo": 6}],
        )


class QueryListActsAsList(TestCase):
    """QueryLists should act just like lists if the wrapper is compatible
    with the src data elements"""

    def setUp(self):
        self.src_list = [{"foo": 1}, {"foo": 2}, {"foo": 3}]
        self.query_list = QueryList(self.src_list)

    def test_QueryList_items_are_equal_to_its_source_lists_items(self):
        self.assertEqual(self.src_list, self.query_list)

    def test_QueryList_length_is_equal_to_its_source_lists_length(self):
        self.assertEqual(len(self.src_list), len(self.query_list))

    def test_QueryLists_can_append_like_lists(self):
        dbl_list = self.src_list + self.src_list
        dbl_query_list = self.query_list + self.query_list

        self.assertEqual(dbl_query_list, dbl_list)

    def test_QueryList_slicing_works_like_list_slicing(self):
        self.assertEqual(self.query_list[:2], self.src_list[:2])

    def test_QueryList_indexing_works_like_list_indexing(self):
        self.assertEqual(self.query_list[1], self.src_list[1])
