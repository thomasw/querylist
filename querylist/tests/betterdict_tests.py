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
    'get': 101,
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

    def test_can_be_used_to_retrieve_dict_keys(self):
        self.assertEqual(self.better_dict.foo, self.src_dict['foo'])

    def test_can_retrieve_keys_that_conflict_with_dict_attrs_via_prefix(self):
        self.assertEqual(self.better_dict._bd_.get, self.src_dict['get'])

    def test_cant_directly_lookup_keys_that_conflict_with_dict_attrs(self):
        self.assertNotEqual(self.better_dict.update, self.src_dict['update'])

class BetterDictDictAttributes(unittest2.TestCase):
    """BetterDict dict attributes"""
    def setUp(self):
        self.src_dict = deepcopy(SRC_DICT)
        self.better_dict = BetterDict(self.src_dict)

    def test_are_converted_to_BetterDicts(self):
        self.assertEqual(
            self.better_dict.bar.another.d,
            self.src_dict['bar']['another']['d'])
