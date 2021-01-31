from unittest import TestCase

from querylist import BetterDict, QueryList
from tests.fixtures import SITE_LIST


class QueryListInstantiationTests(TestCase):
    """QueryList instantiation"""

    def test_sets_wrapper_attribute_to_BetterDict_by_default(self):
        self.assertEqual(QueryList()._wrapper, BetterDict)

    def test_sets_wrapper_attribute_to_value_passed_as_wrapper_to_init(self):
        self.assertEqual(QueryList(wrapper=dict)._wrapper, dict)

    def test_sets_src_data_attirbute_to_iterable_passed_to_constructor(self):
        self.assertEqual(QueryList([1, 2], None).src_data, [1, 2])

    def test_converts_src_data_members_to_wrapper_type(self):
        self.assertEqual(QueryList([1, 2, 3], str), ["1", "2", "3"])

    def test_with_wrap_disabled_doesnt_touch_member_objects(self):
        self.assertEqual(QueryList([1, 2, 3], str, False), [1, 2, 3])


class QueryListConverIterableTests(TestCase):
    """QueryList._convert_iterable()"""

    def setUp(self):
        self.iterable = [{"foo": 1}, {"bar": 2}]
        self.ql = QueryList()

    def test_converts_an_iterables_members_to_BetterDicts_by_default(self):
        converted = self.ql._convert_iterable(self.iterable)
        self.assertEqual(converted[0], BetterDict(self.iterable[0]))

    def test_doesnt_convert_passed_iterable_when_wrapper_attr_is_None(self):
        ql = QueryList(wrapper=None)
        self.assertEqual(ql._convert_iterable(self.iterable), self.iterable)


class QueryListCheckElementTests(TestCase):
    "QueryList._check_element()"

    def setUp(self):
        self.ql = QueryList()
        self.bd = BetterDict({"id": 1, "dog": 4})

    def test_returns_true_if_instance_matches_lookup_value_pairs(self):
        self.assertTrue(self.ql._check_element({"id": 1}, self.bd))

    def test_returns_false_if_instance_doesnt_match_lookup_value_pairs(self):
        self.assertFalse(self.ql._check_element({"id": 2}, self.bd))

    def test_handles_multiple_lookup_value_pairs_correctly(self):
        self.assertTrue(self.ql._check_element({"id": 1, "dog": 4}, self.bd))


class QueryListMethodTests(TestCase):
    def setUp(self):
        self.src_list = SITE_LIST
        self.ql = QueryList(SITE_LIST)


class QueryListCountPropertyTests(QueryListMethodTests):
    "QueryList.count"

    def test_returns_how_many_objects_are_in_the_querylist(self):
        self.assertEqual(self.ql.count, len(self.src_list))


class QueryListGetMethodTests(QueryListMethodTests):
    """QueryList.get()"""

    def test_returns_first_encountered_match(self):
        self.assertEqual(self.ql.get(id=2), self.src_list[1])

    def test_returns_first_element_when_not_passed_anything(self):
        self.assertEqual(self.ql.get(), self.src_list[0])

    def test_raises_an_exception_if_no_matches_are_found(self):
        self.assertRaises(QueryList.NotFound, self.ql.get, url="github.com")

    def test_works_correctly_with_multiple_lookups(self):
        self.assertEqual(
            self.ql.get(id=3, name__iexact="site 3", published=False), self.src_list[2]
        )

    def test_works_correctly_with_relational_lookups(self):
        self.assertEqual(
            self.ql.get(meta__keywords__contains="Catsup"), self.src_list[1]
        )


class QueryListExcludeMethodTests(QueryListMethodTests):
    """QueryList.exclude()"""

    def test_excludes_all_if_passed_nothing(self):
        self.assertEqual(self.ql.exclude(), [])

    def test_excludes_the_matching_set_of_elements(self):
        self.assertEqual(self.ql.exclude(published=True), [self.src_list[2]])

    def test_returns_an_empty_querylist_if_all_items_match(self):
        self.assertFalse(self.ql.exclude(meta__description__icontains="cool site"))


class QueryListFilterMethodTests(QueryListMethodTests):
    """QueryList.filter()"""

    def test_returns_everything_if_it_is_passed_nothing(self):
        self.assertEqual(self.ql.filter(), self.src_list)

    def test_returns_subset_of_matching_elements(self):
        self.assertEqual(self.ql.filter(published=False), [self.src_list[2]])

    def test_returns_an_empty_querylist_if_no_items_match(self):
        self.assertFalse(self.ql.filter(id=1000))
