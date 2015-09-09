from copy import deepcopy

from querylist import BetterDict

from tests.base import TestCase

SRC_DICT = {
    'foo': 1,
    'bar': {
        'a': 0,
        'b': 1,
        'c': 2,
        'another': {
            'd': 0,
            'e': 1,
            'f': 2,
        }
    },
    'get': 101,
    'kittens': False,
    'update': 17,
    '_bd_': 18,
    '_bd_update': 19,
    '_bd__bd_bd_db_silly': 20,
}


class BetterDictTestCase(TestCase):
    def setUp(self):
        self.src_dict = deepcopy(SRC_DICT)
        self.better_dict = BetterDict(self.src_dict)


class BetterDictsDotLookups(BetterDictTestCase):
    """BetterDict dot lookups"""
    def test_can_be_used_to_retrieve_dict_keys(self):
        self.assertEqual(self.better_dict.foo, self.src_dict['foo'])

    def test_can_retrieve_keys_that_conflict_with_dict_attrs_via_prefix(self):
        self.assertEqual(self.better_dict._bd_.get, self.src_dict['get'])

    def test_cant_directly_lookup_keys_that_conflict_with_dict_attrs(self):
        self.assertNotEqual(self.better_dict.update, self.src_dict['update'])

    def test_can_lookup_keys_equal_to_the_prefix_by_using_the_prefix(self):
        self.assertEqual(self.better_dict._bd_._bd_, self.src_dict['_bd_'])


class BetterDictDictAttributes(BetterDictTestCase):
    """BetterDict dict attributes"""
    def test_are_converted_to_BetterDicts(self):
        self.assertEqual(
            self.better_dict.bar.another.d,
            self.src_dict['bar']['another']['d'])


class BetterDictDotAssignment(BetterDictTestCase):
    """BetterDict dot assignment"""
    def test_updates_the_key_corresponding_to_the_attribute_used(self):
        self.better_dict.foo = 2
        self.assertEqual(self.better_dict['foo'], 2)

    def test_updates_the_values_accessed_via_the_prefix(self):
        self.better_dict.foo = 1000
        self.assertEqual(self.better_dict._bd_.foo, 1000)

    def test_updates_keys_that_conflict_with_dict_attrs_without_the_prefix(
            self):
        self.better_dict.update = 'kittens'
        self.assertEqual(self.better_dict['update'], 'kittens')

    def test_updates_correct_key_value_even_if_the_prefix_is_used(
            self):
        self.better_dict._bd_.update = 'updated'
        self.assertEqual(self.better_dict['update'], 'updated')

    def test_can_update_keys_equal_to_the_prefix(self):
        self.better_dict._bd_._bd_ = 800
        self.assertEqual(self.better_dict['_bd_'], 800)

    def test_updates_nested_dictionaries(self):
        self.better_dict.bar.a = 'done!'
        self.assertEqual(self.better_dict.bar.a, 'done!')
        self.assertEqual(self.better_dict['bar']['a'], 'done!')


class BetterDictDirList(BetterDictTestCase):
    "BetterDict dir() list"
    def test_contains_the_BetterDicts_keys(self):
        for key in self.src_dict.keys():
            self.assertIn(key, dir(self.better_dict))

    def test_contains_standard_dict_attrs(self):
        for dict_attr in dir(dict):
            self.assertIn(dict_attr, dir(self.better_dict))

    def test_conatins__bd_(self):
        """contains the attr named '_bd_'"""
        self.assertIn('_bd_', dir(self.better_dict))
