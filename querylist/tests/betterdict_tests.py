from copy import deepcopy
import unittest2

from querylist import BetterDict

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
    'kittens': False,
    'update': 17,
    '_bd_': 18,
    '_bd_update': 19,
    '_bd__bd_bd_db_silly': 20,
}


class BetterDictsDotLookups(unittest2.TestCase):
    """BetterDict dot lookups"""
    def setUp(self):
        self.src_dict = deepcopy(SRC_DICT)
        self.better_dict = BetterDict(self.src_dict)

    def test_can_retrieve_dict_keys(self):
        self.assertEqual(self.better_dict.foo, self.src_dict['foo'])

    def test_can_retrieve_keys_that_conflict_with_dict_attrs_via_prefix(self):
        self.assertEqual(self.better_dict._bd_update, self.src_dict['update'])

    def test_can_lookup_keys_that_start_with_the_prefix_via_prefix(self):
        """can lookup keys that start with '_bd_' by prepending '_bd_' to
        the begging of the key name"""
        self.assertEqual(
            self.better_dict._bd__bd_update, self.src_dict['_bd_update'])

    def test_can_lookup_a_key_equal_to_the_prefix(self):
        self.assertEqual(self.better_dict._bd_, self.src_dict['_bd_'])

    def test_can_lookup_ridiculous_attrs_using_the_prefix(self):
        self.assertEqual(
            self.better_dict._bd__bd__bd_bd_db_silly,
            self.src_dict['_bd__bd_bd_db_silly'])

    def test_will_only_let_you_do_a_prefixed_lookup_if_it_is_necessary(self):
        self.assertRaises(
            AttributeError, getattr, self.better_dict, '_bd_kittens')


class BetterDictDictAttributes(unittest2.TestCase):
    """BetterDict dict attributes"""
    def setUp(self):
        self.src_dict = deepcopy(SRC_DICT)
        self.better_dict = BetterDict(self.src_dict)

    def test_are_converted_to_BetterDicts(self):
        self.assertEqual(
            self.better_dict.bar.another.d,
            self.src_dict['bar']['another']['d'])
