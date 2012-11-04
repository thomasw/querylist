import unittest2

from querylist import BetterDict


class BetterDictActsAsDict(unittest2.TestCase):
    """BetterDicts should act just like dictionaries"""
    def setUp(self):
        self.src_dict = {
            'foo': 1,
            'bar': 2,
            'kitten': 3,
            'update': 4,
        }

        self.better_dict = BetterDict(self.src_dict)

    def test_BetterDict_and_its_src_dictionary_are_equal(self):
        self.assertEqual(self.better_dict, self.src_dict)

    def test_BetterDict_indexing_works_like_dictionary_indexing(self):
        self.assertEqual(self.better_dict['foo'], self.src_dict['foo'])

    def test_BetterDict_assignment_works_like_dictionary_assignment(self):
        self.src_dict['blast'] = 4
        self.better_dict['blast'] = 4

        self.assertEqual(self.better_dict['blast'], self.src_dict['blast'])

    def test_BetterDict_attributes_dont_conflict(self):
        """BetterDicts with keys that conflict with dict attributes should not
        overrride the dict attributes with the key's value"""
        self.better_dict.update({'iron': 'curtain'})

        self.assertEqual(self.better_dict['iron'], 'curtain')
