from querylist.dict import BetterDictLookUp

from querylist.tests.base import TestCase


class BetterDictLookUpInstancesCan(TestCase):
    def setUp(self):
        self.src_dict = {
            'foo': 1,
            'bar': 2,
            'yay': 'kittens'
        }
        self.bdlu = BetterDictLookUp(self.src_dict)

    def test_do_dot_lookups_for_key_values(self):
        self.assertEqual(self.bdlu.foo, self.src_dict['foo'])

    def test_do_dot_assignments_for_key_values(self):
        self.bdlu.yay = False
        self.assertEqual(self.bdlu.yay, self.src_dict['yay'])
